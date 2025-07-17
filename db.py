import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='dfaal496_gesture_transfer',
        password='gesture_transfer1101D',  # Ganti dengan password MySQL kamu
        database='dfaal496_gesture_transfer'
    )
