# High Availability Smart Taxi Distributed System
  
## Introduction
This project aims to build an online Easy Ride Booking system, which enables users to upload their trip orders and helps them to match the drivers by an efficient real-time matching algorithm.<br>More specifically, this project is built up with four major conponents, which is listed as follows:
- **Front-end user interface** <br> Used to interact with the system including registering user account, logging in, making trip order, updating driver's realtime position, updating the trip status, etc.
- **Back-end API** <br> Used to realize the business logic of system including processing the front-end request, proceeding with user inputs, manipulating the databases, etc.
- **Databases** <br> Used to store data of user information, driver information, trip information as well as drivers' realtime position information.
- **Middleware** <br> Used to speed up the process of reading driver's realtime position from front-end and cut down the QPS of Database server.

## Infrastructure ##
Generally, this project is mainly written in **Python** using **Flask** with **MVC** pattern. <br>
- For the front-end user interface, the front-end pages are displayed with **HTML** file. And **JavaScript** is used to develop the dynamic front-end user interface which interacts with back-end API with **XMLHttpRequest**.<br>
- For the back-end API, it is implemented by **Flask** which provides a lot of useful components like make_response, url_for, redirect, etc.<br>
- For the token based authentication, the token is created by the package **itsdangerous**.<br>
- For the uuid which is used as trip id, it is created by the package **uuid**.<br>
- For the database, it is implemented by **PostgreSQL** which communicates with the back-end API using **psycopg2**.<br>
- For the middleware, the double-redis structure is built and controlled by the package **Redis**.

## Detailed Design
- ### Service Structure Design ###
<p align="center">
<img align="center" src="https://github.com/Connor-ZH/GrabTaxi/blob/master/Diagrams/Service_structure.png" alt="drawing" width="500"/>
</p>
<p align="center">Service Structure Diagram</p>
As seen in the diagram, considering the load balance in the real life scenario, the service struture of this project consists of two services, which are Dispatch Service and Geo Service. Dispatch Service is responsible for handling the basic business logic like processing user's request, driver's answer and so on, while Geo Service is reponsible for handling the request of driver's updating realtime position, matching eligible drivers based on an efficient matching algorithm, etc.

- ### Database Design ###
Both of the two services mentioned hava their own database which is implemented in PostgreSQl. The design of the databases is listed as follows:
<p align="center">
<img align="center" src="https://github.com/Connor-ZH/GrabTaxi/blob/master/Diagrams/Database_of_Dispatch_Service.png" alt="drawing" width="500"/>
</p>
<p align="center">Database Design of Dispatch Service</p>
For the Dispatch Service, there are three tables inside its database. The trip table is used to store the detailed information of trips, with two foreign keys, the trip table is linked to the driver table whick stores the information of drivers and the user table which stores the information of users.
<p align="center">
<img align="center" src="https://github.com/Connor-ZH/GrabTaxi/blob/master/Diagrams/Database_of_Geo_Service.png" width="500"/>
</p>
<p align="center">Database Design of Geo Service</p>
For the Geo Service, there are 101 tables inside its database. Among those 101 tables, one is the driver_location_table, which contains the location and the corresponding zone of all the drivers, the other 100 tables contains the location information of the drivers in the corresponding zone. The zones are splited based on the range of driver location. The reason of the tables setting is that it can help with an efficient mataching algorithm to match the nearest drivers, which would be clarified later.

- ### Middleware Design ###
<p align="center">
<img align="center" src="https://github.com/Connor-ZH/GrabTaxi/blob/master/Diagrams/Design of Double Redis Structure.png" width="600"/>
</p>
<p align="center">Design of Double Redis Structure</p>
As seen in the diagram, a Read/Write Splitting Double Redis structure is implemented in this project to cut down the QPS of database server as well as speed up the process of updating driver location query from user. A redis is used as a filter to filter out the driver's request which is going to update the same position. This idea comes from the real life scenario where driver may stay at the same position due to traffic jam. Another redis is used for users to subscribe to their driver's position. A driver id key will be created in the redis once the driver accepts the trip. From then on, the filter will keep updating the driver location in this redis if the corresponding driver key is inside the redis so that the redis does not send query to database too much. Once the trip is done, the corresponding driver id key will be removed from the redis.

- ### Design of Driver Matching Algorithm ###
An efficient driver matching algorithm is put forward in this project which is used to optimize the speed of matching the neraest drivers for the user. Instard of searching the whole driver location table, the driver location table is splited into different zone tables according to their location for searching.
The function to get the corresponding zone of given locations is shown as below:
```
def find_zone(long,lati):
    '''
    find the zone where the driver is
    :param long:
    :param lati:
    :return: if the location is valid, return the corresponding zone otherwise return -1
    '''
    if long < 0 or lati < 0 or long > 90 or lati > 90:
        return -1
    return  (long)//10 + (lati)//10*10
```
Once the user upload their trip order to the dispatch service, the Dispatch Service will send the pickup location in the trip to the Geo Service. Then the Geo Service will use the find_zone funciton to get the corresponding zone of pickup location. After that, the Geo service will call the following get_search_zones function make sure whether it should iterate the driver in other driver_Of_zone tables
```
def get_search_zones(long,lati,distance,origin_zone):
    '''
    judge whether needs to search the drivers in the neighbour zones, if so put the zone into res
    :param long:
    :param lati:
    :param distance:
    :param zone:
    :return: A list of zones to search for nearby drivers
    '''
    final_result = [origin_zone]
    direction_zone_dict = {Direction.Right: find_zone(long, lati + distance), Direction.Left: find_zone(long, lati - distance),
                           Direction.Up: find_zone(long + distance, lati), Direction.Down: find_zone(long - distance, lati)}

    valid_directions = []
    for dir, zone in direction_zone_dict.items():
        if zone != origin_zone and zone != -1:
            valid_directions.append(dir)
            final_result.append(zone)

    if len(valid_directions) >= 2:
        neighbour_zone_direct_dict = {origin_zone + 9: (Direction.Left, Direction.Up), origin_zone + 11: (Direction.Right, Direction.Up),
                                      origin_zone - 11: (Direction.Down, Direction.Left), origin_zone - 9: (Direction.Down, Direction.Right)}

        for neighbour, dir_tuple in neighbour_zone_direct_dict.items():
            if dir_tuple[0] in valid_directions and dir_tuple[1] in valid_directions:
                final_result.append(neighbour)
    return final_result
```
After getting the zones to search, the Geo Service will iterate the driver in all the tables in the final_result returned by the get_search_zones function and calculate their distance to pickup location. After that, an heaptify function is called to sort the distance of the drivers and get the top ten drivers, which would be returned to Dispatch Service.
```
def sort_nearest_drivers(drivers):
    '''
    sort the drivers according to their distance to the pickup location and return the top 10 drivers_id
    :param drivers
    :return: the top 10 drivers_id
    '''
    for index in range((len(drivers)-2)//2,-1,-1):
        bubble_down(drivers,index)
    for i in range(10):
        swap(drivers,0,len(drivers)-1-i)
        bubble_down(drivers,0,len(drivers)-1-i)
    return drivers[-1:-11:-1]

def find_nearest_drivers(pickup_location,distance=4):
    drivers = []
    longitude = pickup_location[0]
    latitude = pickup_location[1]
    zone_of_pickup_location = find_zone(longitude,latitude)
    search_zones = get_search_zones(longitude,latitude,distance,zone_of_pickup_location)
    nearby_drivers = DBhelper.get_nearby_drivers(longitude,latitude,distance,search_zones)
    sorted_drivers = sort_nearest_drivers(nearby_drivers)
    return sorted_drivers
```
So far, the matching algorithm is done.
- ### Design of Token-Based Authentication ###
Since http is a stateless protocol, it would be difficult for server to keep track of user’s state information. And this may result in a bad user experience. For example, to do the identity verification, the user may need to log in for every web page in a shopping platform. One feasible and popular solution to this problem would be making use of cookie and session. In the scenario of identity verification, user only needs to log in for once and the server would store the user status as session on the server side and return the session id as cookie which would be stored on the user side. After that, every time when user send http requests to the platform, the requests would automatically carry the cookie. As a result, server would be able to extract the cookie from the user’s requests and map it to the corresponding session to get the user state information. However, this solution would be considered as defective due to the following reasons: Firstly, for the sake of information safety, Hackers can get user’s cookie by Cross-Site Scripting and deceive the server with the cookie hacked. Apart from that, by the technique of Cross Site Request Forgery, hackers can also trick a web browser into sending unwanted requests which may make the user lose money or something. Secondly, considering a scenario that our system is built on distributed server architecture, it would be a challenge for servers to store and share the session across multi-servers, otherwise the other servers cannot keep track of user’s state. To tackle those issues, there is a more reliable and efficient approach called token-based authentication. The implementation details are as follows: The user’s state information together signature provided by server would be encrypted and passed to user’s local storage by server. And every time the token would be set as one of the headers of the http requests when user side is trying to call some sensitive interface. With the token extracted from user’s request, the server would be able to decrypt the token and verify the identity of users. The major difference between token and cookie is that token won’t be sent by web browsers automatically so that we should not care about the problem of Cross Site Request Forgery or the Cross-Site Scripting. Besides, since the server side does not store any information about the user state, our distributed server structure will not have the problem of sharing session and it would also help save the memory of server.
