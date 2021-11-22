import Dispatch
from Dispatch import controller
from Message import DBhelper as DBhelper
import Dispatch
from datetime import datetime


def insert_message(trip_id, user_id, driver_id):
    DBhelper.insert_message(trip_id, user_id, driver_id)

def update_user_content(trip_id, user_content):
    now = datetime.now()
    user_content_ori = DBhelper.get_user_content(trip_id)
    if user_content_ori:
        user_content= user_content_ori + "  "+ now.strftime("%d/%m/%Y %H:%M:%S") + "  " + user_content
    else:
        user_content = now.strftime("%d/%m/%Y %H:%M:%S") + "  " + user_content
    DBhelper.update_user_content(trip_id, user_content)

def update_driver_content(trip_id, driver_content):
    now = datetime.now()
    driver_content_ori = DBhelper.get_driver_content(trip_id)
    if driver_content_ori:
        driver_content = driver_content_ori+ "  " + now.strftime("%d/%m/%Y %H:%M:%S") + "  " +driver_content
    else:
        driver_content = now.strftime("%d/%m/%Y %H:%M:%S") + "  "+ driver_content
    DBhelper.update_driver_content(trip_id, driver_content)

