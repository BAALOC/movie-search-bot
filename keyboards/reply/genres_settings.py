from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from config_data.config import ALLOWED_GENRES
from database.user_data import User
from keyboards.reply import settings_menu
from loader import bot
from states.user_states import UserState


def genres_gen_markup() -> ReplyKeyboardMarkup:
    genres_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    genres_markup.row(
        KeyboardButton(text='◀️Назад'),
        KeyboardButton(text='Очистить жанры🗑'),
        KeyboardButton(text='Поменять жанр🔧')
    )
    return genres_markup


@bot.message_handler(func=lambda message: message.text == 'Очистить жанры🗑')
def handle_delete_genres(message: Message) -> None:
    user = User.get(User.user_id == message.from_user.id)
    user.genres = None
    user.save()

    bot.send_message(
        message.from_user.id,
        'Твой список жанров теперь пуст',
        reply_markup=settings_menu.settings_gen_markup()
    )


@bot.message_handler(func=lambda message: message.text == 'Поменять жанр🔧')
def handle_delete_genres(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        'Введи жанр, по которому хотите найти фильм. Пример: "драма", "комедия"'
    )
    bot.set_state(message.from_user.id, UserState.genre)


@bot.message_handler(func=lambda message: message.text == '◀️Назад')
def handle_delete_genres(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        'Возвращение в меню настроек',
        reply_markup=settings_menu.settings_gen_markup()
    )


@bot.message_handler(state=UserState.genre)
def bot_get_genres(message: Message) -> None:
    user_id = message.from_user.id
    genre = message.text.strip().lower()

    if genre not in ALLOWED_GENRES:
        bot.send_message(
            user_id,
            'Недопустимый жанр. Пожалуйста, введи один из следующих жанров:\n' +
            ', '.join(ALLOWED_GENRES)
        )
        return

    bot.set_state(message.from_user.id, UserState.base)
    user = User.get(User.user_id == user_id)
    user.genres = genre
    user.save()

    bot.send_message(
        user_id,
        'В поиске по рейтингу теперь будут отображаться фильмы только этого жанра',
        reply_markup=settings_menu.settings_gen_markup()
    )
