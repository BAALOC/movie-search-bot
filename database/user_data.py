from peewee import Model, SqliteDatabase, IntegerField

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)


def create_models():
    db.create_tables(BaseModel.__subclasses__())
