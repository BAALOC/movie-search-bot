from telebot.types import Message

from keyboards.reply import settings_menu
from loader import bot
from utils.check_registration import bot_check_registration


@bot.message_handler(commands=['settings'])
def bot_settings(message: Message) -> None:
    user_id = message.from_user.id

    if not bot_check_registration(user_id):
        bot.send_message(user_id, 'Ты не зарегистрирован! Нажми /start чтобы продолжить')
        return

    bot.send_message(user_id, 'Что хочешь изменить?', reply_markup=settings_menu.settings_gen_markup())
