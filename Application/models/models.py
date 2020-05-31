import os
import sys
from datetime import datetime

from peewee import Model, SqliteDatabase, IntegerField, CharField,  DateField, ForeignKeyField

db = SqliteDatabase(os.path.dirname(sys.argv[0])+'database.db')

class Agent(Model):
    account_id = IntegerField(unique=True)

    class Meta:
        database = db

class User(Model):
    id = IntegerField(unique=True, primary_key=True)
    username = CharField()
    phone = CharField(unique=True, null=False)
    date_of_register = DateField(default=datetime.now)
    agent = ForeignKeyField(Agent, backref="user_id", null=True)

    class Meta:
        database = db

class Indicate(Model):
    account_id = ForeignKeyField(Agent, backref="indicates")
    date = DateField()
    h_kitchen = IntegerField()
    c_kitchen = IntegerField()
    h_bathroom = IntegerField()
    c_bathroom = IntegerField()
    electricity = IntegerField()

    class Meta:
        database = db