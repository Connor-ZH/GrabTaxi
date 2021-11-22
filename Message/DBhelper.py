from Health import DBhelper
from Message import config
import psycopg2
from Common.decorator import *


class Helper:
    def __init__(self):
        self.connection = psycopg2.connect(database=config.database_name,
                                           user=config.user_name,
                                           password=config.password,
                                           port=config.port,
                                           )
        self.cursor = self.connection.cursor()
    
    # @log_error_db
    def create_message_table(self):
        # create_message_table
        query = "CREATE TABLE message_table(" \
                "trip_id TEXT PRIMARY KEY," \
                "user_id BIGINT,"\
                "driver_id BIGINT," \
                "user_content TEXT," \
                "driver_content TEXT," \
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" \
                ");"
        self.cursor.execute(query)
        self.connection.commit()
    
    @log_error_db
    def insert_message(self, trip_id, user_id, driver_id):
        trip_id = str(trip_id)
        query = "INSERT INTO message_table" \
                "(trip_id, user_id, driver_id)" \
                f" VALUES ('{trip_id}', '{user_id}','{driver_id}');"
        self.cursor.execute(query)
        self.connection.commit()

    def update_user_content(self, trip_id, user_content):
        trip_id = str(trip_id)
        query = "UPDATE message_table " \
                f"SET user_content='{user_content}' " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        self.connection.commit()

    def update_driver_content(self, trip_id, driver_content):
        trip_id = str(trip_id)
        query = "UPDATE message_table " \
                f"SET driver_content='{driver_content}' " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        self.connection.commit()

    def get_user_content(self,trip_id):
        trip_id = str(trip_id)
        query = "SELECT user_content FROM message_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        user_content = self.cursor.fetchall()[0][0]
        return user_content

    def get_driver_content(self,trip_id):
        trip_id = str(trip_id)
        query = "SELECT driver_content FROM message_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        driver_content = self.cursor.fetchall()[0][0]
        return driver_content

    def roll_back(self):
        self.cursor.execute("ROLLBACK")
