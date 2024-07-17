from telebot.types import Message

from database.user_data import User
from loader import bot


# user_messages = ['привет', 'старт', 'начало', 'start', '/start']
# Доделать обработку ключевых слов

@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    full_name = message.from_user.full_name

    if not user:
        User.create(user_id=user_id)
        text = f'Привет, {full_name}!'
    else:
        text = f'Снова рад тебя видеть, {full_name}!'

    bot.send_message(user_id, text)
