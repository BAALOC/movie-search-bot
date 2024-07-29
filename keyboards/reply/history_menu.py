from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from database.user_data import Movie
from handlers.custom_handlers import history
from keyboards.inline import history_pagination
from loader import bot
from states.user_states import UserState


def history_menu_gen_markup():
    history_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    history_menu_markup.row(
        KeyboardButton(text='⏪Назад'),
        KeyboardButton(text='История📖'),
        KeyboardButton(text='Поиск по дате🔎')
    )
    return history_menu_markup


@bot.message_handler(func=lambda message: message.text == 'История📖')
def handle_history(message: Message) -> None:
    history.bot_history(message)


@bot.message_handler(func=lambda message: message.text == 'Поиск по дате🔎')
def handle_history(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Введи дату в формате (ДД.ММ.ГГГГ), за которую хочешь посмотреть историю поиска'
    )
    bot.set_state(message.from_user.id, UserState.date)


@bot.message_handler(state=UserState.date)
def get_date(message: Message):
    date_string = message.text
    user_id = message.from_user.id
    try:
        movies = Movie.select().where(
            Movie.user == user_id,
            Movie.date == date_string
        ).order_by(Movie.date.desc(), Movie.movie_id.desc())
        if not movies:
            bot.send_message(
                message.chat.id,
                'По такой дате фильм не найден, для продолжения ещё раз введи команду',
                reply_markup=history_menu_gen_markup()
            )
            bot.set_state(user_id, UserState.base)
            return

        bot.set_state(user_id, UserState.base)
        history_pagination.send_movie_page(message, list(movies))

    except ValueError:
        bot.send_message(message.from_user.id, 'Введи дату в формате (ДД.ММ.ГГГГ)')
