from Common.enum import *
from Health import DBhelper as DBhelper



def update_user_health_status(user_id,pulse,temperature):
    user_status = Health_status.Normal
    if temperature < 36.5 or temperature >37.5 or pulse <60 or pulse > 100:
        user_status = Health_status.Abnormal
    try:
        DBhelper.update_user_health_status(user_id,pulse,temperature,user_status)
    except:
        DBhelper.insert_user_health_status(user_id, pulse, temperature,user_status)
    return user_status

def update_driver_health_status(driver_id,pulse,temperature,BAC):
    driver_status = Health_status.Normal
    if temperature < 36.5 or temperature >37.5 or pulse <60 or pulse > 100 or BAC > 0.08:
        driver_status = Health_status.Abnormal
    try:
        DBhelper.update_driver_health_status(driver_id,pulse,temperature,BAC,driver_status)
    except:
        DBhelper.insert_driver_health_status(driver_id, pulse,temperature,BAC, driver_status)
    return driver_status

