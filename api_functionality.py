import sys
import logging
import json
import requests


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