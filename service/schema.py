import jsl

CREATE_ROLE = 'create'
MOCK_ROLE = 'mock'
true_if_create = jsl.Var({
    jsl.not_(MOCK_ROLE): True
})
LOGIN_ROLE = 'login'
REGISTER_ROLE = 'register'
true_if_register = jsl.Var({
    jsl.not_(LOGIN_ROLE): True
})


class User(jsl.Document):
    username = jsl.StringField(required=True)
    password = jsl.StringField(required=True, min_length=8)
    email = jsl.StringField(required=true_if_register)


class Category(jsl.Document):
    name = jsl.StringField(required=True, min_length=3, max_length=15)
    description = jsl.StringField(max_length=50)


class Spend(jsl.Document):
    date = jsl.StringField(required=true_if_create)
    price = jsl.IntField(required=true_if_create)
    category = jsl.StringField(required=true_if_create, min_length=3)
