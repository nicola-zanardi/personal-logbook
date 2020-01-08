from peewee import SqliteDatabase, DateTimeField, CharField, Model, BooleanField
import datetime
from flask_login import UserMixin

db = SqliteDatabase("logbook/logbook.db")


class LogItem(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    content = CharField()

    class Meta:
        database = db


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([LogItem, User])
