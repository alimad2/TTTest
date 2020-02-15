from mongoengine import *

connect('spends')


class Spend(Document):
    id = IntField(required=True, primary_key=True)
    date = StringField(required=True)
    price = IntField(required=True)
    on = StringField(required=True, max_length=50)
