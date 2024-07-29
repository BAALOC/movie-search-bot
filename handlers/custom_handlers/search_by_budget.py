from telebot.types import Message

from api.api import api_search_by_budget
from keyboards.inline import pagination
from keyboards.reply import main_menu
from loader import bot
from utils import check_registration, handle_movie_result, validate_history


@bot.message_handler(func=lambda message: message.text in ['/low_budget_movie', '/high_budget_movie'])
def bot_search_by_budget(message: Message) -> None:
    user_id = message.from_user.id
    bot.send_message(
        user_id,
        'Твой запрос обрабатывается, это может занять какое-то время',
        reply_markup=main_menu.main_menu_gen_markup()
    )
    if not check_registration.bot_check_registration(user_id):
        bot.send_message(user_id, 'Ты не зарегистрирован! Нажми /start чтобы продолжить')
        return

    try:
        result = api_search_by_budget(user_id=user_id, command=message.text[1:])
        if not handle_movie_result.bot_handle_movie_result(user_id=user_id, result=result):
            return
    except Exception as exc:
        bot.send_message(
            user_id,
            f'Произошла ошибка: {exc}. Введи команду ещё раз',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return

    movie_info = pagination.get_movie_info(result=result)
    validate_history.bot_validate_history(user_id=user_id, movie_info=movie_info)
    pagination.bot_send_movie_page(user_id=user_id, data_dict=result)
