import psycopg2


def create_tables(conn):
    query_create_sensors_table = "CREATE TABLE sensors (id SERIAL PRIMARY KEY, type VARCHAR(50), eui64 VARCHAR(50));"
    cursor = conn.cursor()
    cursor.execute(query_create_sensors_table)
    conn.commit()
    cursor.close()

    query_create_sensordata_table = """CREATE TABLE sensor_data (
                                               time TIMESTAMPTZ NOT NULL,
                                               sensor_id INTEGER,
                                               temperature DOUBLE PRECISION,
                                               FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                               );"""
    query_create_sensordata_hypertable = "SELECT create_hypertable('sensor_data', 'time');"


def write(conn, sensor_data):
    sql_sensors_insert = "INSERT INTO sensors (type, eui64) VALUES (%s, %s);"
    cursor = conn.cursor()
    try:
        data = (sensor_data[0], sensor_data[1])
        cursor.execute(sql_sensors_insert, data)
    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)
    conn.commit()

def write_data(conn, sensor_data):
    sql_data_insert = "INSERT INTO sensor_data(time, sensor_id, temperature) VALUES(%s, %s, %s)"


def main():
    with psycopg2.connect(CONNECTION) as conn:
        cursor = conn.cursor()
        # use the cursor to interact with your database
        cursor.execute("SELECT * FROM table")
        print(cursor.fetchone())
