"""
Declaring parameter to use to establish connection with database
author: Marco Aldana
"""
import pymysql
from peewee import MySQLDatabase
from project.database.constants import DB_DATABASE, DB_USER, DB_PORT, DB_HOST, DB_PASSWORD

connect = MySQLDatabase(
    DB_DATABASE,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


def create_database():
    flag = True
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    my_cursor = conn.cursor()
    my_cursor.execute('Show databases;')
    for db in my_cursor:
        flag = False if DB_DATABASE == db[0] else flag
    if flag:
        conn.cursor().execute(f'CREATE DATABASE {DB_DATABASE};')
    conn.close()

# show status where variable_name = 'threads_connected';
