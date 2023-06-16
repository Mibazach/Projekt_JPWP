import json
import api_functionality


def find_movies(search_input):
    returned_movies_str = api_functionality.get_movies_req(search_input)
    returned_movies_json = json.loads(returned_movies_str)
    if returned_movies_json['Response'] != 'False':
        return returned_movies_json["Search"]
    else:
        return None
print(find_movies("dsadasdds"))