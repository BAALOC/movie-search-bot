from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


# user_messages = ['помощь', 'help', '/help']
# Доделать обработку ключевых слов


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    text = '\n'.join(f'/{command}   -   {info}' for command, info in DEFAULT_COMMANDS)
    bot.send_message(message.chat.id, f'Вот мой список команд:\n\n{text}')
