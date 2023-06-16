import json
import api_functionality

returned_movies_str = api_functionality.get_movies_req("Friends")  # String
returned_movies_json = json.loads(returned_movies_str)  # JSON

print(returned_movies_str)
print()
print(returned_movies_json["Search"][0], type(returned_movies_json["Search"]))

# api_functionality.add_movie_to_db(1, returned_movies_json["Search"][0], 7)

"""
if returned_movies_json['Response'] != 'False':
    for movie in returned_movies_json["Search"]:
        print(movie)
else:
    print('Movie not found!')
"""
"""
Zakładam na razie takie dwie tabele z takimi kolumnami:

user: | user_id | login | password | 
movie: | movie_id | title | year | type | poster | posted_by | 

"""
