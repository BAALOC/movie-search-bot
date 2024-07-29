from telebot.types import Message

from api.api import api_movie_search
from config_data.config import BUTTONS_TEXT
from keyboards.inline import pagination
from keyboards.reply import main_menu
from loader import bot
from states.user_states import UserState
from utils import validate_history, handle_movie_result, check_registration


@bot.message_handler(commands=['movie_search'])
def bot_movie_search(message: Message) -> None:
    user_id = message.from_user.id

    if not check_registration.bot_check_registration(user_id):
        bot.send_message(
            user_id,
            'Ты не зарегистрирован! Нажми /start чтобы продолжить',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return

    bot.send_message(
        message.chat.id,
        'Введи название фильма, который хочешь найти\n\nПример: "Начало"',
        reply_markup=main_menu.main_menu_gen_markup()
    )
    bot.set_state(message.from_user.id, UserState.search)


@bot.message_handler(state=UserState.search)
def get_movie_name(message: Message) -> None:
    user_id = message.from_user.id
    try:
        movie_name = message.text.strip()
        if movie_name in BUTTONS_TEXT:
            bot.send_message(
                user_id,
                'Ошибка! Надо ввести название фильма, а не команду',
                reply_markup=main_menu.main_menu_gen_markup()
            )
            bot.set_state(user_id, UserState.base)
            return

        result = api_movie_search(movie_name=movie_name, user_id=user_id)
        if not handle_movie_result.bot_handle_movie_result(user_id=user_id, result=result):
            return

    except Exception as exc:
        bot.send_message(
            user_id,
            f'Произошла ошибка: {exc}. Введи команду ещё раз',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        bot.set_state(user_id, UserState.base)
        return

    bot.set_state(user_id, UserState.base)

    movie_info = pagination.get_movie_info(result=result)
    validate_history.bot_validate_history(user_id=user_id, movie_info=movie_info)
    pagination.bot_send_movie_page(user_id=user_id, data_dict=result)
