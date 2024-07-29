from telebot.types import Message

from database.user_data import Movie
from keyboards.inline import history_pagination
from keyboards.reply import main_menu
from loader import bot
from utils import check_registration


@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    user_id = message.from_user.id
    if not check_registration.bot_check_registration(user_id):
        bot.send_message(
            user_id,
            'Ты не зарегистрирован! Нажми /start чтобы продолжить',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return

    movies = Movie.select().where(Movie.user == user_id).order_by(Movie.date.desc(), Movie.movie_id.desc())
    if not movies:
        bot.send_message(
            message.chat.id,
            'Твоя история поиска пуста',
            reply_markup=main_menu.main_menu_gen_markup()
        )
        return

    history_pagination.send_movie_page(message=message, data=list(movies))
