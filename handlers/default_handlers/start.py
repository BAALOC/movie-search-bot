from telebot.types import Message

from database.user_data import User
from keyboards.reply import main_menu
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    full_name = message.from_user.full_name

    if not user:
        User.create(user_id=user_id)
        greeting = (
            f'👋 Привет, {full_name}! Я - бот, который позволяет искать фильмы и сериалы прямо из '
            'чата в Telegram 🎬📺. Я помогу тебе найти интересные фильмы и популярные сериалы, а также '
            'предоставлю информацию о них. Чтобы продолжить, выбери одну из команд ниже 👇'
        )
    else:
        greeting = (
            f'👋 Снова рад тебя видеть, {full_name}! Я помогу тебе искать фильмы и сериалы 🎬📺. '
            'Ты уже знаешь, как это работает. Чтобы продолжить, выбери одну из команд ниже 👇'
        )

    bot.send_message(user_id, greeting, reply_markup=main_menu.main_menu_gen_markup())
