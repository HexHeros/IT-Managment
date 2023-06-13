import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Get database credentials from environment variables
host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USER")
passwd = os.environ.get("DB_PASSWORD")
db = os.environ.get("DB_NAME")

def connect_to_database():
    '''
    Connects to the database and returns a database connection object.
    '''
    db_connection = MySQLdb.connect(host, user, passwd, db)
    return db_connection

def execute_query(db_connection, query, query_params=()):
    '''
    Executes a given SQL query on the given database connection and returns a Cursor object.
    '''
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    db_connection.commit()
    return cursor

# Rest of your code...
