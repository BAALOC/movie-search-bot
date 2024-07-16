from telebot.types import Message

from api.api import api_movie_search
from loader import bot
from states.user_states import UserState
from utils.check_registration import bot_check_registration
from keyboards.inline.pagination import bot_send_movie_page, get_movie_info
from utils.validate_history import bot_validate_history


@bot.message_handler(commands=['movie_search'])
def bot_movie_search(message: Message) -> None:
    user_id = message.from_user.id

    if not bot_check_registration(user_id):
        bot.send_message(user_id, 'Ты не зарегистрирован! Нажми /start чтобы продолжить')
        return

    bot.send_message(message.chat.id, 'Введи название фильма, который хочешь найти\n\nПример: "Начало"')
    bot.set_state(message.from_user.id, UserState.search)


@bot.message_handler(state=UserState.search)
def get_movie_name(message: Message) -> None:
    user_id = message.from_user.id
    try:
        movie_name = message.text.strip().lower()
        result = api_movie_search(movie_name=movie_name, user_id=user_id)
        handle_movie_result(user_id=user_id, result=result)

    except Exception as exc:
        bot.send_message(user_id, f'Произошла ошибка: {exc}')
        return

    bot.set_state(user_id, UserState.base)

    movie_info = get_movie_info(result=result)
    bot_validate_history(user_id=user_id, movie_info=movie_info)
    bot_send_movie_page(user_id=user_id, data_dict=result)


def handle_movie_result(user_id: int, result: dict) -> None:
    if not result:
        bot.send_message(user_id, 'Ошибка! Попробуй снова')
        return
    if not result['docs']:
        bot.send_message(user_id, 'Такого фильма не найдено')
        return
