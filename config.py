import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload')
    MENU_IMAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'img')