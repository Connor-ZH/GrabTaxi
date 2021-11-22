from Geo.DBhelper import Helper
from Common.util import *
from Common.enum import *
from Geo import DBhelper as DBhelper
from Filter import controller as filter
from Redis import controller as redis
import numpy as np
import time
import random
import matplotlib.pyplot as plt


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
            if neighbour >= 0 and dir_tuple[0] in valid_directions and dir_tuple[1] in valid_directions:
                final_result.append(neighbour)
    return final_result

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

# change a matching sort algorithm for performance check
def sort_nearest_drivers_SelectionSort(drivers):
    n = len(drivers)
    for i in range(n - 1, 0, -1):
        maxIdx = i
        for j in range(i):
            if drivers[j].distance > drivers[maxIdx].distance:
                maxIdx = j
        drivers[i], drivers[maxIdx] = drivers[maxIdx], drivers[i]
    return drivers[:10]

# driver matching without process optimization
def find_nearest_drivers_without_matching_optimization(longitude, latitude, distance=4):
    nearby_drivers = DBhelper.get_nearby_drivers_without_search_zones(longitude, latitude, distance)
    sorted_drivers = sort_nearest_drivers_SelectionSort(nearby_drivers)
    # print("Based on the naive matching method, the selected available drivers are (by ID & distance):")
    # for driver in sorted_drivers:
    #     print(f"{driver.id}({driver.distance})", end=", ")
    # print()
    return sorted_drivers

# driver matching with process optimization
def find_nearest_drivers_with_matching_optimization(longitude, latitude, distance=4):
    zone_of_pickup_location = find_zone(longitude,latitude)
    search_zones = get_search_zones(longitude,latitude,distance,zone_of_pickup_location)
    nearby_drivers = DBhelper.get_nearby_drivers(longitude,latitude,distance,search_zones)
    sorted_drivers = sort_nearest_drivers(nearby_drivers)
    # print("Based on the optimized matching method, the selected available drivers are (by ID & distance):")
    # for driver in sorted_drivers:
    #     print(f"{driver.id}({driver.distance})", end=", ")
    # print()
    return sorted_drivers

def find_nearest_drivers(pickup_location,distance=4):
    longitude = pickup_location[0]
    latitude = pickup_location[1]

    # check matching process without optimization
    # start_time1 = time.time()
    sorted_drivers_without_optimization = find_nearest_drivers_without_matching_optimization(longitude, latitude, distance)
    # y1 = (time.time() - start_time1) * 1000
    # print(f"The matching process takes {y1:.3f} ms")
    # print()

    # check matching with optimization
    # start_time2 = time.time()
    sorted_drivers_with_optimization = find_nearest_drivers_with_matching_optimization(longitude, latitude, distance)
    # y2 = (time.time() - start_time2) * 1000
    # print(f"The matching process takes {y2:.3f} ms")
    # print()
    return sorted_drivers_with_optimization
    # return y1, y2

def get_driver_location(driver_id):
    return DBhelper.get_driver_location(driver_id)

def update_driver_location(driver_id,longitude,latitude, with_filter=True):
    if with_filter == False:
        DBhelper.update_driver_location(driver_id, longitude, latitude)
        return
    pre_longitude, pre_latitude = filter.get_driver_location(driver_id)
    if np.random.choice([True,False], 1,replace=True, p=[0.2, 0.8]) and pre_latitude and pre_longitude:
        longitude = pre_longitude
        latitude = pre_latitude
    if (pre_latitude == None and pre_latitude == None) or (pre_longitude != longitude or pre_latitude != latitude):
        DBhelper.update_driver_location(driver_id, longitude, latitude)
        filter.update_driver_location(driver_id,longitude,latitude)
        longitude_in_redis, latitude_in_redis = redis.get_driver_location_without_database(driver_id)
        if longitude_in_redis != None:
            redis.update_driver_location(driver_id,longitude,latitude)


# Used for the performance measurement
# if __name__ == "__main__":
#     worldMap = [i for i in range(90)]
#     y1 = []
#     y2 = []
#     x = [i for i in range(3000)]
#     for _ in range(3000):
#         print(_)
#         pickup_location = random.sample(worldMap, 2)
#         process_time1, process_time2 = find_nearest_drivers(pickup_location, distance=4)
#         y1.append(process_time1)
#         y2.append(process_time2)
    
#     # plotting
#     plt.plot(x, y1, label="Naive Matching")
#     plt.plot(x, y2, label="Optimized Matching")
#     plt.xlabel("Number of Matchings")
#     plt.ylabel("Matching Processing Time (ms)")
#     plt.legend()
#     plt.title("Comparison of Driver Matching Methods")
#     plt.show()
