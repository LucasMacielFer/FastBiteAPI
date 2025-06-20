from DB_connect import *
import os
from dotenv import load_dotenv

load_dotenv()

db = os.getenv("MYSQL_DATABASE")
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
conn = connect(host, db, user, password, port)

print(send_query(conn, "select * from users;"))