from telebot.types import Message

from api.api import api_movie_by_rating
from database.user_data import User
from keyboards.inline import pagination
from keyboards.reply import main_menu
from loader import bot
from states.user_states import UserState
from utils import check_registration, validate_history, handle_movie_result


@bot.message_handler(commands=['movie_by_rating'])
def bot_movie_by_rating(message: Message) -> None:
    user_id = message.from_user.id

    if not check_registration.bot_check_registration(user_id):
        bot.send_message(
            user_id,
            'Ты не зарегистрирован! Нажми /start чтобы продолжить',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return
    user = User.get(User.user_id == user_id)
    if user.genres:
        text = ('Введи рейтинг в диапазоне от 0 до 10, по которому будет происходить поиск. Пример: "7", "8", "7-9"'
                f'\n\nТвой список жанров: {user.genres}')
    else:
        text = ('Введи рейтинг в диапазоне от 0 до 10, по которому будет происходить поиск. Пример: "7", "8", "7-9"'
                '\n\nТвой список жанров пуст')

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu.main_menu_gen_markup()
    )
    bot.set_state(message.from_user.id, UserState.rating)


@bot.message_handler(state=UserState.rating)
def get_movie_rating(message: Message) -> None:
    user_id = message.from_user.id
    try:
        rating = validate_rating(rating=message.text.strip())
        result = api_movie_by_rating(rating=rating, user_id=user_id)
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


def validate_rating(rating: str) -> str:
    if '-' in rating:
        min_rating, max_rating = map(float, rating.split('-'))
        if not (0 <= min_rating <= 10 and 0 <= max_rating <= 10 and min_rating <= max_rating):
            raise ValueError('Диапазон рейтинга должен быть в пределах от 0 до 10 и корректным')
    else:
        rating = float(rating)
        if not 0 <= rating <= 10:
            raise ValueError('Рейтинг должен быть в диапазоне от 0 до 10')
        min_rating = max(rating - 1, 0)
        max_rating = min(rating + 1, 10)
        rating = f'{min_rating:.1f}-{max_rating:.1f}'

    return rating
