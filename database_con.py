import mysql.connector
import sys
import logging
import json


def data_base_connect():
    logging.info("Opening cred file")
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)
    except IOError:
        logging.critical("Couldn't load cred file")
        sys.exit(1)
    else:
        host = data["host"]
        user = data["user"]
        password = data["password"]
        database = data["database"]
        logging.info("Cred saved")

    try:
        logging.info("Starting database connection...")
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except mysql.connector.errors.Error:
        logging.critical("Application couldn't connect to the database. Closing application")
        sys.exit(2)
    else:
        logging.info("Application connected to the database successfully")
        return mydb

