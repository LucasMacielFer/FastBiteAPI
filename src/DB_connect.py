import mysql.connector

def connect(host, database, user, password, port):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)
        print(f"Connected succesfully to database {database} on MySQL.")

    except Exception as e:
        print(f"Failed to connect to database {database} on MySQL.")
    return conn

def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed.")

def send_query(conn, query):
    cursor = conn.cursor()
    result = None
    desc = None

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        desc = [d[0] for d in cursor.description]
    except Exception as e:
        print("Invalid search on database.")
    cursor.close()
    
    return result, desc