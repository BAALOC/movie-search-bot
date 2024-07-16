from telegram_bot_pagination import InlineKeyboardPaginator

from loader import bot

user_data = {}


def bot_send_movie_page(user_id: int, data_dict: dict, page: int = 1) -> None:
    user_data[user_id] = data_dict
    paginator = InlineKeyboardPaginator(
        len(data_dict['docs']),
        current_page=page,
        data_pattern='movie_page#{page}'
    )

    info = get_movie_info(data_dict, page)

    bot.send_message(
        user_id,
        text=info,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


def get_movie_info(result: dict, page: int = 1) -> str:
    movie_info = result['docs'][page - 1]
    text_dict = {
        'Название': movie_info.get('name', 'Название недоступно'),
        'Описание': movie_info.get('description', 'Описание недоступно'),
        'Рейтинг': round(movie_info.get('rating', {}).get('imdb', 0), 1),
        'Год производства': movie_info.get('year', 'Год неизвестен'),
        'Жанр': ', '.join(genre['name'] for genre in movie_info.get('genres', [])),
        'Возрастной рейтинг': movie_info.get('ageRating', 'N/A'),
        'Постер': movie_info.get('poster', {}).get('url', 'Постер недоступен')
    }
    result_string = '\n'.join(
        f'{name}: {info}\n' if info else f'{name}: <пусто>\n'
        for name, info in text_dict.items()
    )

    return result_string


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'movie_page')
def movie_page_callback(call) -> None:
    page = int(call.data.split('#')[1])
    user_id = call.from_user.id

    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot_send_movie_page(user_id=user_id, data_dict=user_data[user_id], page=page)
