from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    base = State()
    search = State()
    rating = State()
    genre = State()
    search_limit = State()
    date = State()
