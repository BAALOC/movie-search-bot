from telebot.custom_filters import StateFilter

import handlers  # noqa
from database.user_data import create_models
from loader import bot
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    create_models()
    set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
