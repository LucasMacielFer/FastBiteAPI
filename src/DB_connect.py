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

def send_query(conn, query, params):
    cursor = conn.cursor()
    result = None
    desc = None

    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        if cursor.description:
            desc = [d[0] for d in cursor.description]
    except Exception as e:
        print("Invalid search on database.")
    cursor.close()
    
    return result, desc

def insert_delete(conn, query, params):
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print("Invalid insertion/deletion on database.")
        conn.rollback()
        return False
    cursor.close()
    return True

def insert_and_get_ID(conn, query, params):
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        id_gerado = cursor.lastrowid
        conn.commit()
    except Exception as e:
        print("Invalid insertion/deletion on database.")
        conn.rollback()
        return -1
    cursor.close()
    return id_gerado