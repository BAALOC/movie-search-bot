import telebot

from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: telebot.TeleBot) -> None:
    bot.set_my_commands(
        [telebot.types.BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
