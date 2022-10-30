import mysql.connector
from mysql.connector import Error

import os

from player import Player

host = os.environ['db_host']
user = os.environ['db_user']
passwd = os.environ['db_pass']
database = os.environ['db_database']


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def get_connection():
    return create_connection(host, user, passwd, database)


def get_top_players():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('select * from csstats order by kills desc limit 15')
    result = cursor.fetchall()
    connection.disconnect()
    players = []
    for i in range(len(result)):
        players.append(Player(i + 1, result[i]))
    return players


if __name__ == '__main__':
    for player in get_top_players():
        print(player)
