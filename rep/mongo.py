from mongoengine import *

connect('spends')


class Category(Document):
    name = StringField(required=True, min_length=3, max_length=15, primary_key=True)
    description = StringField(max_length=50)


class Spend(Document):
    id = IntField(required=True, primary_key=True)
    date = StringField(required=True)
    price = IntField(required=True)
    category = ReferenceField(Category, reverse_delete_rule=CASCADE)
