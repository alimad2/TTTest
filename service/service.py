from rep.mongo import Spend, Category, User
from mongoengine import *


def find_id():
    max_id = 0
    for spend in Spend.objects:
        if spend.id > max_id:
            max_id = spend.id
    return max_id + 1


def create_spend(spend):
    id = find_id()
    flag = False
    c = spend['category']
    for category in Category.objects:
        if category.name == c:
            flag = True
    if not flag:
        return False
    spends = Spend(id=id, date=spend['date'], price=spend['price'], category=spend['category']).save()
    return spends


def find_spend(spend_id):
    for spend in Spend.objects():
        if spend.id == spend_id:
            return spend


def update_spend(spend_id, sp):
    if not (1 <= spend_id < find_id()):
        return False
    spend = find_spend(spend_id)
    if sp.price != 'nothing':
        spend.price = sp.price
    if sp.date != 'nothing':
        spend.date = sp.date
    if sp.on != 'nothing':
        spend.on = sp.on
    spend.save()
    return spend


def get_all(price, date, page, category, per_page):
    if page is None:
        page = 1
    if per_page is None:
        per_page = 5
    page = int(page)
    items_per_page = int(per_page)
    offset = (page - 1) * items_per_page
    spends = []
    if price is not None:
        for spend in Spend.objects(price__gte=price).skip(offset).limit(items_per_page):
            spends.append(spend)
    if date is not None:
        for spend in Spend.objects(date=date).skip(offset).limit(items_per_page):
            spends.append(spend)
    if category is not None:
        for spend in Spend.objects(category=category).skip(offset).limit(items_per_page):
            spends.append(spend)
    if date is None and price is None and category is None:
        for spend in Spend.objects().skip(offset).limit(items_per_page):
            spends.append(spend)
    return spends


def get_this_spend(spend_id):
    if not (1 <= spend_id < find_id()):
        return False
    return find_spend(spend_id)


def delete_spend(spend_id):
    if not (1 <= spend_id < find_id()):
        return False
    spend = find_spend(spend_id)
    spend.delete()


def create_category(category):
    category = Category(name=category['name'], description=category['description']).save()
    return category
