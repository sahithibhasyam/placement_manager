import mysql.connector
from mysql.connector import Error
import settings as sett

def connect_database():
    try:
        sett.connection = mysql.connector.connect(
            host=sett.DB_HOST,
            database=sett.DB_NAME,
            user=sett.DB_USER,
            password=sett.DB_PASSWORD
        )
        sett.mycursor = sett.connection.cursor()
        print("Connected to MySQL Server")
    except Error as e:
        print("Error while connecting to MySQL", e)

def disconnect_database():
    if sett.mycursor and sett.connection:
        sett.mycursor.close()
        sett.connection.close()
        print("MySQL connection is closed")
