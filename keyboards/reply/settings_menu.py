from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from database.user_data import User, Movie
from keyboards.reply import genres_settings, main_menu
from loader import bot
from states.user_states import UserState


def settings_gen_markup() -> ReplyKeyboardMarkup:
    settings_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    settings_markup.row(
        KeyboardButton(text='Настроить поиск⌨️'),
        KeyboardButton(text='Настроить жанры🕹')
    )
    settings_markup.row(
        KeyboardButton(text='⏪Назад'),
        KeyboardButton(text='Удалить историю поиска🗑')
    )
    return settings_markup


def confirmation_gen_markup() -> ReplyKeyboardMarkup:
    confirmation_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    confirmation_markup.row(
        KeyboardButton(text='Удалить✅'),
        KeyboardButton(text='Не удалять❌')
    )
    return confirmation_markup


@bot.message_handler(func=lambda message: message.text == 'Настроить поиск⌨️')
def handle_search_settings(message: Message) -> None:
    user = User.get(User.user_id == message.from_user.id)
    bot.send_message(
        message.chat.id,
        'Сколько фильмов должно выводиться в результате поиска? (от 1 до 250).'
        f'\nТвои текущие настройки: {user.search_limit}',
        reply_markup=settings_gen_markup()
    )
    bot.set_state(message.from_user.id, UserState.search_limit)


@bot.message_handler(func=lambda message: message.text == 'Настроить жанры🕹')
def handle_search_settings(message: Message) -> None:
    user = User.get(User.user_id == message.from_user.id)

    if user.genres:
        text = f'Что ты хочешь изменить?\n\nТвой выбор жанров: {user.genres}'
    else:
        text = 'Что ты хочешь изменить?\n\nУ тебя нет выбранного жанра'

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=genres_settings.genres_gen_markup()
    )


@bot.message_handler(func=lambda message: message.text == 'Удалить историю поиска🗑')
def handle_search_settings(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Ты точно хочешь удалить свою историю поиска?',
        reply_markup=confirmation_gen_markup()
    )


@bot.message_handler(func=lambda message: message.text == '⏪Назад')
def handle_search_settings(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Возвращение в главное меню',
        reply_markup=main_menu.main_menu_gen_markup()
    )


@bot.message_handler(func=lambda message: message.text in ['Удалить✅', 'Не удалять❌'])
def handle_delete_confirmation(message: Message) -> None:
    if message.text == 'Удалить✅':
        Movie.delete().where(Movie.user == message.from_user.id).execute()
        bot.send_message(
            message.chat.id,
            'История поиска полностью очищена✅',
            reply_markup=settings_gen_markup()
        )
    elif message.text == 'Не удалять❌':
        bot.send_message(
            message.chat.id,
            'Ты отменил действие, история поиска осталась',
            reply_markup=settings_gen_markup()
        )


@bot.message_handler(state=UserState.search_limit)
def bot_get_search_limit(message: Message):
    user_id = message.from_user.id
    try:
        search_limit = int(message.text)
        if not 1 <= search_limit <= 250:
            bot.send_message(
                user_id,
                'Ошибка: Введи целое число от 1 до 250',
                reply_markup=settings_gen_markup()
            )
            return

        bot.set_state(message.from_user.id, UserState.base)
        user = User.get(User.user_id == user_id)
        user.search_limit = search_limit
        user.save()

        bot.send_message(
            user_id,
            f'Настройки обновлены! Теперь в результатах поиска будет выводиться {search_limit} фильмов',
            reply_markup=settings_gen_markup()
        )

    except Exception as exc:
        bot.set_state(message.from_user.id, UserState.base)
        bot.send_message(
            user_id,
            f'Произошла ошибка: {exc}. Введи команду ещё раз',
            reply_markup=settings_gen_markup()
        )
        return
