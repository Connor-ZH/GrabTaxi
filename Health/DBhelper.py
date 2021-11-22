from Health import config
import psycopg2
from Common.enum import *
from Common.decorator import *


class Helper:
    def __init__(self):
        self.connection = psycopg2.connect(database=config.database_name,
                                           user=config.user_name,
                                           password=config.password,
                                           port=config.port,
                                           )
        self.cursor = self.connection.cursor()

    @log_error_db
    def insert_driver_health_status(self, driver_id,pulse,temperature,BAC,status):
        query = "INSERT INTO driver_health_status_table " \
                "(driver_id,pulse,temperature,BAC,status)" \
                f"VALUES ('{driver_id}','{pulse}', '{temperature}', '{BAC}', '{status.value}');"
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def insert_user_health_status(self, user_id,pulse,temperature,status):
        query = "INSERT INTO user_health_status_table " \
                "(user_id,pulse,temperature,status)" \
                f"VALUES ('{user_id}','{pulse}', '{temperature}','{status.value}');"
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def get_user_health_status_detail(self, user_id):
        print(user_id)
        query = "SELECT pulse,temperature,updated_at,status FROM user_health_status_table " \
                f"WHERE user_id = '{user_id}'"
        self.cursor.execute(query)
        self.connection.commit()
        res = self.cursor.fetchall()
        pulse = res[0][0]
        temperature = res[0][1]
        updated_at = res[0][2]
        status = res[0][3]
        print(pulse, temperature, updated_at, status)
        return pulse, temperature, updated_at, status

    @log_error_db
    def get_driver_health_status_detail(self, driver_id):
        query = "SELECT * FROM driver_health_status_table " \
                f"WHERE driver_id = '{driver_id}'"
        self.cursor.execute(query)
        self.connection.commit()
        res = self.cursor.fetchall()
        pulse = res[0][0]
        temperature = res[0][1]
        BAC = res[0][2]
        updated_at = res[0][3]
        status = res[0][4]
        return pulse, temperature,BAC, updated_at,status

    @log_error_db
    def create_user_health_status_table(self):
        # create_trip_table
        query = "CREATE TABLE user_health_status_table(" \
                "user_id BIGINT PRIMARY KEY," \
                "pulse SMALLINT," \
                "temperature NUMERIC," \
                "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP," \
                "status smallint" \
                ");"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def create_driver_health_status_table(self):
        # create_trip_table
        query = "CREATE TABLE driver_health_status_table(" \
                "driver_id BIGINT PRIMARY KEY," \
                "pulse SMALLINT," \
                "temperature NUMERIC," \
                "blood_alcohol_concentration NUMERIC," \
                "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP," \
                "status smallint" \
                ");"
        self.cursor.execute(query)
        self.connection.commit()

    def update_user_health_status(self, user_id,pulse,temperature,status):
        query = "UPDATE user_health_status_table " \
                f"SET status = {status.value} ," \
                f"pulse = {pulse}," \
                f"temperature = {temperature}," \
                f"updated_at = now() " \
                f"WHERE user_id = '{user_id}';"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def update_driver_health_status(self,driver_id,pulse,temperature,BAC,status):
        query = "UPDATE driver_health_status_table " \
                f"SET status = {status.value} ," \
                f"pulse = {pulse}," \
                f"temperature = {temperature}," \
                f"blood_alcohol_concentration = {BAC}," \
                f"updated_at = now() " \
                f"WHERE driver_id = '{driver_id}';"
        self.cursor.execute(query)
        self.connection.commit()
