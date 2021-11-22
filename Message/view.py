from Message import controller as controller


def create_message(trip_id, content):
    controller.insert_message(trip_id, content)
