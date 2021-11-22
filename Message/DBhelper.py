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
                "message_id BIGSERIAL PRIMARY KEY," \
                "trip_id TEXT," \
                "content TEXT," \
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" \
                ");"
        self.cursor.execute(query)
        self.connection.commit()
    
    @log_error_db
    def insert_message(self, trip_id, content):
        query = "INSERT INTO message_table" \
                "(trip_id, content)" \
                f" VALUES ('{trip_id}', '{content}');"
        self.cursor.execute(query)
        self.connection.commit()
