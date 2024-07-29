from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from api.api import api_search_by_budget
from database.user_data import User
from handlers.custom_handlers import movie_search, movie_by_rating, settings
from handlers.default_handlers import help
from keyboards.inline import pagination
from keyboards.reply import history_menu
from loader import bot
from utils import handle_movie_result, validate_history
from utils.check_registration import bot_check_registration


def main_menu_gen_markup() -> ReplyKeyboardMarkup:
    main_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    main_menu_markup.row(
        KeyboardButton(text='Поиск по названию🔎'),
        KeyboardButton(text='Поиск по рейтингу📈'),
        KeyboardButton(text='Поиск по бюджету💸')
    )
    main_menu_markup.row(
        KeyboardButton(text='Помощь📲'),
        KeyboardButton(text='История поиска📖'),
        KeyboardButton(text='Настройки⚙️')
    )
    return main_menu_markup


def budget_menu_gen_markup() -> ReplyKeyboardMarkup:
    budget_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    budget_menu_markup.row(
        KeyboardButton(text='⏪Назад'),
        KeyboardButton(text='По низкому бюджету📉'),
        KeyboardButton(text='По высокому бюджету📈')
    )
    return budget_menu_markup


@bot.message_handler(func=lambda message: message.text == 'Поиск по названию🔎')
def handle_search_by_name(message: Message) -> None:
    movie_search.bot_movie_search(message)


@bot.message_handler(func=lambda message: message.text == 'Поиск по рейтингу📈')
def handle_search_by_rating(message: Message) -> None:
    movie_by_rating.bot_movie_by_rating(message)


@bot.message_handler(func=lambda message: message.text == 'Поиск по бюджету💸')
def handle_search_by_budget(message: Message) -> None:
    user_id = message.from_user.id
    if not bot_check_registration(user_id):
        bot.send_message(
            user_id,
            'Ты не зарегистрирован! Нажми /start чтобы продолжить',
            reply_markup=main_menu_gen_markup()
        )
        return

    user = User.get(User.user_id == user_id)
    if user.genres:
        text = f'Какой поиск хочешь выбрать?\n\nТвой текущий выбор жанров: {user.genres}'
    else:
        text = 'Какой поиск хочешь выбрать?\n\nУ тебя нет выбранного жанра'

    bot.send_message(message.chat.id, text, reply_markup=budget_menu_gen_markup())


@bot.message_handler(func=lambda message: message.text == 'Помощь📲')
def handle_help(message: Message) -> None:
    help.bot_help(message)


@bot.message_handler(func=lambda message: message.text == 'История поиска📖')
def handle_search_history(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Какое действие хочешь совершить?',
        reply_markup=history_menu.history_menu_gen_markup()
    )


@bot.message_handler(func=lambda message: message.text == 'Настройки⚙️')
def handle_settings(message: Message) -> None:
    settings.bot_settings(message)


@bot.message_handler(func=lambda message: message.text in [
    'По низкому бюджету📉',
    'По высокому бюджету📈'
])
def handle_all_messages(message: Message) -> None:
    user_id = message.from_user.id
    bot.send_message(
        user_id,
        'Твой запрос обрабатывается, это может занять какое-то время',
        reply_markup=budget_menu_gen_markup()
    )

    if message.text == 'По высокому бюджету📈':
        result = api_search_by_budget(user_id=user_id, command='high_budget_movie')
    else:
        result = api_search_by_budget(user_id=user_id, command='low_budget_movie')

    movie_info = pagination.get_movie_info(result=result)
    validate_history.bot_validate_history(user_id=user_id, movie_info=movie_info)
    handle_movie_result.bot_handle_movie_result(user_id=user_id, result=result)
    pagination.bot_send_movie_page(user_id=user_id, data_dict=result)
