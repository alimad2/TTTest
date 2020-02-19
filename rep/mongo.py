from flask_login import UserMixin
from mongoengine import *

from app import login_manager

connect('spends')


@login_manager.user_loader
def load_user(user_id):
    users = User.objects(username=user_id)
    return users[0]


class User(Document, UserMixin):
    username = StringField(required=True, primary_key=True)
    password = StringField(required=True, min_length=8)
    email = StringField(required=True)
    name = StringField()


class Category(Document):
    id = StringField(primary_key=True)
    name = StringField(required=True, min_length=3, max_length=15)
    description = StringField(max_length=50, required=True)
    owner = ReferenceField('User', reverse_delete_rule=CASCADE, required=True)


class Spend(Document):
    id = IntField(primary_key=True)
    date = StringField(required=True)
    price = IntField(required=True)
    category = ReferenceField('Category', reverse_delete_rule=CASCADE, required=True)
    owner = ReferenceField('User', reverse_delete_rule=CASCADE, required=True)
