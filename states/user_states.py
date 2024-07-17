from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    base = State()
    search = State()
    rating = State()
