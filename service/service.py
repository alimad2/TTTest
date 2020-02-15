from rep.mongo import Spend


def find_id():
    max_id = 0
    for spend in Spend.objects:
        if spend.id > max_id:
            max_id = spend.id
    return max_id + 1


def create_spend(spend):
    id = find_id()
    spend = Spend(id=id, date=spend['date'], price=spend['price'], on=spend['on']).save()
    return spend


def find_spend(spend_id):
    for spend in Spend.objects:
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


def get_all():
    spends = []
    for spend in Spend.objects:
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


def spend_on(on):
    spends = []
    for spend in Spend.objects(on=on):
        spends.append(spend)
    return spends


def spend_price(price):
    spends = []
    for spend in Spend.objects(price__gte=price):
        spends.append(spend)
    return spends


def spend_date(date):
    spends = []
    for spend in Spend.objects(date=date):
        spends.append(spend)
    return spends
