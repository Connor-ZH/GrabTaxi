from Health import controller as controller
from Common.enum import *


def update_user_health_status(user_id,pulse,temperature):
    user_status = controller.update_user_health_status(user_id,pulse,temperature,)
    return user_status

def update_driver_health_status(driver_id,pulse,temperature,BAC):
    driver_status = controller.update_driver_health_status(driver_id,pulse,temperature,BAC)
    return driver_status


