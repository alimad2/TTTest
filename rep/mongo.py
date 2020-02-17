from mongoengine import *
from flask_login import UserMixin
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
    name = StringField(required=True, min_length=3, max_length=15, primary_key=True)
    description = StringField(max_length=50)


class Spend(Document):
    id = IntField(required=True, primary_key=True)
    date = StringField(required=True)
    price = IntField(required=True)
    category = ReferenceField(Category, reverse_delete_rule=CASCADE)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
