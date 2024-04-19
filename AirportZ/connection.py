import mysql.connector

def get_connection():

    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='testi',
        user='root',
        password='As1allinenSalauS',
        autocommit=True
        )
    return connection