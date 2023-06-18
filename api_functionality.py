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


def add_movie_to_db(username, movie_information_json, rating, review):
    try:
        mydb = database_con.data_base_connect()
        my_cursor = mydb.cursor()
        title = movie_information_json['Title']
        year = movie_information_json['Year']
        poster = movie_information_json['Poster']
        query = f'SELECT * FROM movies WHERE title = %s AND posted_by = %s'
        my_cursor.execute(query, (title, username))
        if my_cursor.fetchall() != 0:
            print('Ten film już został dodany do profilu')
            mydb.close()
            return
        query = 'INSERT INTO movies (title, year, poster, posted_by, posted_when ,rating, review)' \
                ' VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)'
        my_cursor.execute(query, (title, year, poster, username, rating, review))
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


# add_movie_to_db("testuser", {'Title': 'Shrek 2', 'Year': '2004', 'imdbID': 'tt0298148', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMDJhMGRjN2QtNDUxYy00NGM3LThjNGQtMmZiZTRhNjM4YzUxL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, "10/10", "slay")
