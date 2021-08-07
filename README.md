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
- ### Service Structure ###
<p align="center">
<img align="center" src="https://github.com/Connor-ZH/GrabTaxi/blob/master/Diagrams/Service_structure.png" alt="drawing" width="500"/>
</p>
## Test
