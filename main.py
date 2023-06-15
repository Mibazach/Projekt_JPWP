import database_con
import api_functionality
import logging
import json
import gui


logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

gui


"""
Zakładam na razie takie dwie tabele z takimi kolumnami:

user: | user_id | login | password | 
movie: | movie_id | title | year | type | poster | posted_by | 

"""


"""
returned_movies_str = api_functionality.get_movies_req("Star Wars")
returned_movies_json = json.loads(returned_movies_str)

if returned_movies_json['Response'] != 'False':
    for movie in returned_movies_json["Search"]:
        print(movie)
else:
    print('Movie not found!')
"""