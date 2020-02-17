from rep.mongo import Spend, Category, User
from mongoengine import *
from mongoengine.queryset.visitor import Q


def find_user(username):
    users = User.objects(username=username)
    return users[0]


def find_id():
    max_id = 0
    for spend in Spend.objects():
        if spend.id > max_id:
            max_id = spend.id
    return max_id + 1


def find_category(username, category_name):
    category_id = str(username) + str(category_name)
    categories = Category.objects(id=category_id)
    return categories[0]


def create_spend(username, spend):
    owner = find_user(username)
    category_name = spend['category']
    categoryy = find_category(username, category_name)
    id = find_id()
    flag = False
    c = spend['category']
    for category in Category.objects(owner=owner):
        if category.name == c:
            flag = True
    if not flag:
        return False
    spends = Spend(owner=owner, id=id, date=spend['date'], price=spend['price'], category=categoryy).save()
    return spends


def find_spend(username, spend_id):
    owner = find_user(username)
    for spend in Spend.objects(owner=owner):
        if spend.id == spend_id:
            return spend


def update_spend(username, spend_id, sp):
    if not (1 <= spend_id < find_id()):
        return False
    spend = find_spend(username, spend_id)
    if sp.price != 'nothing':
        spend.price = sp.price
    if sp.date != 'nothing':
        spend.date = sp.date
    if sp.on != 'nothing':
        spend.on = sp.on
    spend.save()
    return spend


def get_all(username, price, date, page, category, per_page):
    owner = find_user(username)
    category = find_category(username, category)
    if page is None:
        page = 1
    if per_page is None:
        per_page = 5
    page = int(page)
    items_per_page = int(per_page)
    offset = (page - 1) * items_per_page
    spends = []
    if price is not None:
        for spend in Spend.objects(Q(owner=owner) & Q(price__gte=price)).skip(offset).limit(items_per_page):
            spends.append(spend)
    if date is not None:
        for spend in Spend.objects(Q(owner=owner) & Q(date=date)).skip(offset).limit(items_per_page):
            spends.append(spend)
    if category is not None:
        for spend in Spend.objects(Q(owner=owner) & Q(category=category)).skip(offset).limit(items_per_page):
            spends.append(spend)
    if date is None and price is None and category is None:
        for spend in Spend.objects(owner=owner).skip(offset).limit(items_per_page):
            spends.append(spend)
    return spends


def get_this_spend(username, spend_id):
    if not (1 <= spend_id < find_id()):
        return False
    return find_spend(username, spend_id)


def delete_spend(username, spend_id):
    owner = find_user(username)
    if not (1 <= spend_id < find_id()):
        return False
    spend = find_spend(owner, spend_id)
    spend.delete()


def create_category(username, category):
    user = find_user(username)
    category = Category(id=str(username) + str(category['name']), name=category['name'],
                        description=category['description'], owner=user).save()
    return category


def get_all_categories(username):
    user = find_user(username)
    categories = Category.objects(owner=user)
    return categories
