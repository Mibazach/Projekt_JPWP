import logging
import gui
import api_functionality
import json

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)



"""
Zakładam na razie takie dwie tabele z takimi kolumnami:

user: | user_id | login | password | 
movie: | movie_id | title | year | type | poster | posted_by | 

"""