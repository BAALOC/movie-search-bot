import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

DB_PATH = 'database.db'
BASE_API_KEY = 'https://api.kinopoisk.dev/v1.4'
DATE_FORMAT = "%d.%m.%Y"

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Справка по боту'),
    ('movie_search', 'Поиск по названию'),
    ('movie_by_rating', 'Поиск по рейтингу'),
    ('history', 'История поиска')
)
