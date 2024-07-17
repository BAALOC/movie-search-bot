import requests
from typing import Dict

from config_data.config import BASE_API_KEY, API_KEY
from database.user_data import User

headers = {
    'accept': 'application/json',
    'X-API-KEY': API_KEY
}


def get_request(endpoint: str, params: dict = None) -> Dict:
    response = requests.get(
        f'{BASE_API_KEY}/{endpoint}',
        headers=headers,
        params=params
    )
    if response.status_code == 200:
        return response.json()


def api_movie_search(movie_name: str, user_id: int) -> Dict:
    user = User.get(User.user_id == user_id)
    endpoint = 'movie/search'
    params = {
        'page': 1,
        'limit': user.search_limit,
        'query': movie_name
    }
    result = get_request(endpoint=endpoint, params=params)
    return result


def api_movie_by_rating(rating: str, user_id: int) -> Dict:
    user = User.get(User.user_id == user_id)
    endpoint = 'movie'
    params = {
        'page': 1,
        'limit': user.search_limit,
        'rating.imdb': rating
    }
    result = get_request(endpoint=endpoint, params=params)
    return result


def api_search_by_budget(user_id: int, command: str) -> Dict:
    user = User.get(User.user_id == user_id)
    endpoint = 'movie'
    params = {
        'page': 1,
        'limit': user.search_limit,
        'budget.value': '100000-5000000' if command == 'low_budget_movie' else '20000000-1000000000'
    }
    result = get_request(endpoint=endpoint, params=params)
    return result

