from database.user_data import User


def bot_check_registration(user_id):
    user = User.get_or_none(User.user_id == user_id)
    if user:
        return True
    return False
