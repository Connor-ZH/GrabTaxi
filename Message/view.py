from Message import controller as controller

def create_message(trip_id, user_id, driver_id):
    controller.insert_message(trip_id, user_id, driver_id)

def update_user_content(trip_id, user_content):
    controller.update_user_content(trip_id,user_content)

def update_driver_content(trip_id, driver_content):
    controller.update_driver_content(trip_id, driver_content)
