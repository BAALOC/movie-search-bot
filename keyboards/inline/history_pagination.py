from telebot.types import Message
from loader import bot
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton
from database.user_data import Movie

user_data = {}


def send_movie_page(message: Message, data, page=1):
    user_id = message.from_user.id
    user_data[user_id] = data
    paginator = InlineKeyboardPaginator(
        len(data),
        current_page=page,
        data_pattern='history_page#{page}'
    )

    movie = user_data[user_id][page - 1]
    if not movie.is_watched:
        paginator.add_before(
            InlineKeyboardButton('Удалить', callback_data=f'delete#{page}'),
            InlineKeyboardButton('Просмотрено', callback_data=f'watched#{page}')
        )
    else:
        paginator.add_before(
            InlineKeyboardButton('Удалить', callback_data=f'delete#{page}'),
            InlineKeyboardButton('Не просмотрено', callback_data=f'watched#{page}')
        )

    text = f'Дата поиска: {movie.date} | {'Просмотрено✅' if movie.is_watched else 'Не просмотрено❌'}\n{movie.info}'

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'history_page')
def movie_page_callback(call):
    page = int(call.data.split('#')[1])
    user_id = call.from_user.id

    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_movie_page(call.message, user_data[user_id],  page)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'delete')
def delete_movie_callback(call):
    page = int(call.data.split('#')[1])
    user_id = call.from_user.id
    watched_movie = user_data[user_id][page - 1]

    movie = Movie.get(user=user_id, info=watched_movie.info)
    movie.delete_instance()
    user_data[user_id].remove(watched_movie)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    if user_data[user_id]:
        send_movie_page(call.message, user_data[user_id],  max(1, page - 1))
    else:
        bot.send_message(
            call.message.chat.id,
            'Ваша история поиска пуста.'
        )


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'watched')
def mark_movie_watched_callback(call):
    page = int(call.data.split('#')[1])
    user_id = call.from_user.id
    watched_movie = user_data[user_id][page - 1]

    if watched_movie.is_watched:
        watched_movie.is_watched = False
    else:
        watched_movie.is_watched = True
    watched_movie.save()

    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_movie_page(call.message, user_data[user_id],  max(1, page))
