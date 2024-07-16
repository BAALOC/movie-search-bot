from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    AutoField,
    ForeignKeyField,
    DateField,
    BooleanField
)

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    search_limit = IntegerField(default=10)


class Movie(BaseModel):
    movie_id = AutoField()
    user = ForeignKeyField(User, backref='movies')
    info = CharField()
    date = DateField()
    is_watched = BooleanField(default=False)


def create_models():
    db.create_tables(BaseModel.__subclasses__())
