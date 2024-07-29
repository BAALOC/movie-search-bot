from keyboards.reply import main_menu
from loader import bot


def bot_handle_movie_result(user_id: int, result: dict) -> bool:
    if not result:
        bot.send_message(
            user_id,
            'Ошибка! Попробуй снова',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return False
    if not result['docs']:
        bot.send_message(
            user_id,
            'Такого фильма не найдено',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return False
    return True
