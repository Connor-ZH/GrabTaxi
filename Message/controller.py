import Dispatch
from Dispatch import controller
from Message import DBhelper as DBhelper
import Dispatch

def insert_message(trip_id, content):
    DBhelper.insert_message(trip_id, content)
