timescaledb_init = "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"

query_create_sensors_table = "CREATE TABLE sensors (id SERIAL PRIMARY KEY," \
                             "type VARCHAR(50)," \
                             "location VARCHAR(50));"

query_create_sensordata_table = "CREATE TABLE sensor_data (" \
                                "time TIMESTAMPTZ NOT NULL," \
                                "sensor_id INTEGER," \
                                "temperature DOUBLE PRECISION," \
                                "FOREIGN KEY (sensor_id) REFERENCES sensors (id)" \
                                ");"
