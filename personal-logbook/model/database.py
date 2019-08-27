from peewee import SqliteDatabase, DateTimeField, CharField, Model
import datetime

db = SqliteDatabase("logbook.db")


class LogItem(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    content = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([LogItem])
