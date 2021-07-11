from Database import config as config
import psycopg2

def build_connection():
    connection = psycopg2.connect(database=config.database_name,
                                  user=config.user_name,
                                  password=config.password,
                                  port=config.port,
                                  )
    return connection

def create_trip_table():
    # create_trip_table
    connection = build_connection()
    cursor = connection.cursor()
    query = "CREATE TABLE trip_table(" \
            "trip_id TEXT PRIMARY KEY," \
            "user_id BIGINT," \
            "driver_id BIGINT," \
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP," \
            "finished_at TIMESTAMP," \
            "status TEXT," \
            "driver_id_refused BIGINT[]," \
            "pickup_location DECIMAL[]," \
            "dropoff_location DECIMAL[]" \
            ");"
    cursor.execute(query)
    connection.commit()
    connection.close()

def create_user_table():
    # create_user_table
    connection = build_connection()
    cursor = connection.cursor()
    query = "CREATE TABLE user_table(" \
            "driver_id BIGSERIAL PRIMARY KEY," \
            "driver_name TEXT," \
            "phone_number VARCHAR(8)," \
            "password TEXT," \
            "trip_id TEXT);"
    cursor.execute(query)
    connection.commit()
    connection.close()

def create_driver_table():
    # create_driver_table
    connection = build_connection()
    cursor = connection.cursor()
    query = "CREATE TABLE driver_table(" \
            "driver_id BIGSERIAL PRIMARY KEY," \
            "driver_name TEXT," \
            "phone_number VARCHAR(8)," \
            "password TEXT," \
            "trip_id TEXT);"
    cursor.execute(query)
    connection.commit()
    connection.close()