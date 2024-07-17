from loader import bot


def bot_handle_movie_result(user_id: int, result: dict) -> bool:
    if not result:
        bot.send_message(user_id, 'Ошибка! Попробуй снова')
        return False
    if not result['docs']:
        bot.send_message(user_id, 'Такого фильма не найдено')
        return False
    return True
