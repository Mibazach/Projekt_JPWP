import sys
import logging
import json
import mysql.connector.errors
import requests
import database_con


def get_movies_req(movie_title):
    movie_title = str(movie_title)
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)
    except IOError:
        logging.critical("Couldn't load cred file")
        sys.exit(1)
    else:
        api_key = data["api_key"]

    try:
        url = f"http://www.omdbapi.com/?apikey={api_key}&s={movie_title}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
    except ConnectionError:
        logging.critical("Coudln't connect to the api")
        sys.exit(3)
    else:
        return response.text


def add_movie_to_db(user_id, movie_information_json, rating):
    try:
        mydb = database_con.data_base_connect()
        my_cursor = mydb.cursor()
        title = movie_information_json['Title']
        year = movie_information_json['Year']
        type = movie_information_json['Type']
        poster = movie_information_json['Poster']
        query = 'INSERT INTO movies (title, year, type, poster, posted_by, posted_when ,rating)' \
                ' VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)'
        my_cursor.execute(query, (title, year, type, poster, user_id, rating))
        mydb.commit()
        mydb.close()
    except mysql.connector.errors.DatabaseError:
        print('cos poszlo nie tak')
        return 0
    else:
        print('dodano recorda')
        return 1


def find_movies(search_input):
    returned_movies_str = get_movies_req(search_input)
    returned_movies_json = json.loads(returned_movies_str)
    if returned_movies_json['Response'] != 'False':
        return returned_movies_json["Search"]
    else:
        return None

