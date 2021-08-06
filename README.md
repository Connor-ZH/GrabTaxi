# High Availability Smart Taxi Distributed System
  
## Introduction
This project aims to build an online Easy Ride Booking system, which enables users to upload their trip orders and helps them to match the drivers according to their pickup location and drivers' realtime position.<br>More specifically, this project is built up with four major conponents, which is listed as follows:
- **Front-end user interface** <br> Used to interact with the system including registering user account, logging in, making trip order, updating driver's realtime position, updating the trip status, etc.
- **Back-end API** <br> Used to realize the business logic of system including processing the front-end request, proceeding with user inputs, manipulating the databases, etc.
- **Databases** <br> Used to store data of user information, driver information, trip information as well as drivers' realtime position information.
- **Middleware** <br> Used to speed up the process of reading driver's realtime position from front-end and cut down the QPS of Database server.

## Infrastructure ##
Generally, this project is mainly written in **Python** using **Flask** with **MVC** pattern. 
<br>For the front-end user interface, the front-end pages are displayed with **HTML** file. And **JavaScript** are used to develop the dynamic front-end user interface with the help of 
And **SQL** is used to manipulate the data stored in the database.

## Detailed Design

## Test
