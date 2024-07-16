import requests

from config_data.config import BASE_API_KEY, API_KEY
from database.user_data import User

headers = {
    'accept': 'application/json',
    'X-API-KEY': API_KEY
}


def get_request(endpoint, params=None):
    response = requests.get(
        f'{BASE_API_KEY}/{endpoint}',
        headers=headers,
        params=params
    )
    if response.status_code == 200:
        return response.json()


def api_movie_search(movie_name, user_id):
    user = User.get(User.user_id == user_id)
    endpoint = 'movie/search'
    params = {
        'page': 1,
        'limit': user.search_limit,
        'query': movie_name
    }
    result = get_request(endpoint, params)
    return result
