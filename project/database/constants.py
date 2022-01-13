"""
Constants for interaction with database
author: Marco Aldana
"""
import json

DB_DATABASE = 'gods_among_us_data'
DB_USER = 'root'
DB_PASSWORD = 'Admin'
DB_HOST = 'localhost'
DB_PORT = 3306

with open("GoogleOauth2.json") as jsonFile:
    JSON_DATA=json.load(jsonFile)

CLIENT_ID = JSON_DATA['client_id']
CLIENT_SECRET = JSON_DATA['client_secret']
