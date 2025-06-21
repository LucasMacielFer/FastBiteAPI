import mysql.connector
from flask import current_app

def get_connection():
    conn = None
    config = current_app.config
    try:
        conn = mysql.connector.connect(
            host=config["MYSQL_HOST"],
            database=config["MYSQL_DATABASE"],
            user=config["MYSQL_USER"],
            password=config["MYSQL_PASSWORD"],
            port=config["MYSQL_PORT"])

    except Exception as e:
        print(f"Failed to connect to database.")
    return conn

def close_connection(conn):
    if conn:
        conn.close()

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