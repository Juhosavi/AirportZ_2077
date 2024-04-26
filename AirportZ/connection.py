import mysql.connector

def get_connection():

    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='testgame',
        user='root',
        password='mariacat123',
        autocommit=True
        )
    return connection