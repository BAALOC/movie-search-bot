from database.user_data import Movie
from datetime import datetime
from config_data.config import DATE_FORMAT


def bot_validate_history(user_id: int, movie_info: str) -> None:
    movies = Movie.select().where(Movie.user == user_id).order_by(Movie.movie_id)

    if movies.count() >= 100:
        movies[0].delete_instance()

    movie, created = Movie.get_or_create(
        user=user_id,
        info=movie_info,
        date=datetime.now().strftime(DATE_FORMAT)
    )

    if not created:
        if movie.is_watched:
            movie.delete_instance()
            Movie.create(user=user_id, date=datetime.now().strftime(DATE_FORMAT), info=movie_info, is_watched=True)
        else:
            movie.delete_instance()
            Movie.create(user=user_id, date=datetime.now().strftime(DATE_FORMAT), info=movie_info)
