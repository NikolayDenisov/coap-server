from config import CONNECTION
import psycopg2
from datetime import datetime

def print_table_values(conn, table, funct, param):
    cursor = conn.cursor()
    if funct == 'first':
        cursor.execute("SELECT " + param[0] + ", first(" + param[1] + ", time) FROM " + table + " GROUP BY " + param[0] + ";")
    elif funct == 'last':
        cursor.execute("SELECT " + param[0] + ", last(" + param[1] + ", time) FROM " + table + " GROUP BY " + param[0] + ";")
    elif funct == 'all':
        cursor.execute("SELECT * FROM " + table + ";")
    elif funct == 'count':
        cursor.execute("ANALYZE " + table + "; SELECT * FROM approximate_row_count('" + table + "');")
    for row in cursor.fetchall():
        print(row)
    cursor.close()

if __name__ == '__main__':
    conn = psycopg2.connect(CONNECTION)
    print_table_values(conn, 'sensor_data', 'count', ['sensor_id', 'temperature'])
