"""
Blueprints for tables in database
author: Marco Aldana
"""
import hashlib
from datetime import datetime
from project.database.connection import connect as db

from peewee import Model, PrimaryKeyField, ForeignKeyField, CharField, DateTimeField, IntegerField, TextField, \
    BooleanField


class User(Model):
    id = PrimaryKeyField()
    username = CharField(max_length=50, unique=True, null=False)
    full_name = CharField(max_length=50, null=False)
    email = CharField(max_length=50, unique=True, null=False)
    password = CharField(max_length=50)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'users'

    @classmethod
    def authenticate(cls, username, password):
        user = cls.select().where(User.username == username).first()

        if user and user.password == cls.create_password(password):
            return user

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()


class Card(Model):
    id = PrimaryKeyField()
    name = CharField(null=False)
    attack = IntegerField(null=False)
    defense = IntegerField(null=False)
    type = CharField(null=False)
    civilization = CharField(null=False)
    description = TextField()
    image = CharField(default="")
    owner = ForeignKeyField(User, null=False)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'cards'


class Deck(Model):
    id = PrimaryKeyField()
    name= CharField(max_length=50, null=False)
    card = ForeignKeyField(Card)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'decks'
