from telebot.types import Message

from api.api import api_movie_search
from keyboards.inline.pagination import bot_send_movie_page, get_movie_info
from loader import bot
from states.user_states import UserState
from utils import validate_history, handle_movie_result
from utils.check_registration import bot_check_registration


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
        if not handle_movie_result.bot_handle_movie_result(user_id=user_id, result=result):
            return

    except Exception as exc:
        bot.send_message(user_id, f'Произошла ошибка: {exc}. Введи команду ещё раз')
        bot.set_state(user_id, UserState.base)
        return

    bot.set_state(user_id, UserState.base)

    movie_info = get_movie_info(result=result)
    validate_history.bot_validate_history(user_id=user_id, movie_info=movie_info)
    bot_send_movie_page(user_id=user_id, data_dict=result)
