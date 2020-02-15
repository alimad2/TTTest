from flask import Blueprint, request, abort, jsonify

import service.service as service

blue = Blueprint('test', __name__)


class Spss():
    def __init__(self, price, date, on):
        self.price = price
        self.date = date
        self.on = on


@blue.route('/spends', methods=['GET'])
def get_all():
    spends = service.get_all()
    spendsJSON = []
    for spend in spends:
        temp = {
            'id': spend.id,
            'date': spend.date,
            'price': spend.price,
            'on': spend.on
        }
        spendsJSON.append(temp)
    return jsonify({'spends': spendsJSON})


@blue.route('/spends/<int:spend_id>', methods=['GET'])
def get_spend(spend_id):
    spend = service.get_this_spend(spend_id)
    if spend == False:
        abort(404)
    spendjson = {
        'id': spend.id,
        'date': spend.date,
        'price': spend.price,
        'on': spend.on
    }
    return jsonify({'spend': spendjson})


@blue.route('/spends', methods=['POST'])
def new_spend():
    if not request.json:
        abort(400)
    spend = {
        'date': request.json['date'],
        'price': request.json['price'],
        'on': request.json['on']
    }
    spend = service.create_spend(spend)
    spendjson = {
        'id': spend.id,
        'date': spend.date,
        'price': spend.price,
        'on': spend.on
    }
    return jsonify({'spend': spendjson})


@blue.route('/spends/<int:spend_id>', methods=['PUT'])
def update_spend(spend_id):
    sp = Spss(request.json.get('price', 'nothing'), request.json.get('date', 'nothing'),
              request.json.get('on', 'nothing'))
    ret = service.update_spend(spend_id, sp)
    if ret == False:
        abort(404)
    spend = {
        'id': ret.id,
        'date': ret.date,
        'price': ret.price,
        'on': ret.on
    }
    return jsonify({'spend': spend})


@blue.route('/spends/<int:spend_id>', methods=['DELETE'])
def delete_spend(spend_id):
    ret = service.delete_spend(spend_id)
    if ret == False:
        abort(404)
    return jsonify({'result': True})


@blue.route('/spends/on/<string:on>', methods=['GET'])
def spends_on(on):
    spends = service.spend_on(on)
    spendsJSON = []
    for spend in spends:
        temp = {
            'id': spend.id,
            'date': spend.date,
            'price': spend.price,
            'on': spend.on
        }
        spendsJSON.append(temp)
    return jsonify({'spends': spendsJSON})


@blue.route('/spends/price/<int:price>', methods=['GET'])
def spend_price(price):
    spends = service.spend_price(price)
    spendsJSON = []
    for spend in spends:
        temp = {
            'id': spend.id,
            'date': spend.date,
            'price': spend.price,
            'on': spend.on
        }
        spendsJSON.append(temp)
    return jsonify({'spends': spendsJSON})


@blue.route('/spends/date/<int:year>/<string:month>/<int:day>')
def spend_date(year, month, day):
    date = str(day) + " " + month + " " + str(year)
    print(date)
    spends = service.spend_date(date)
    spendsJSON = []
    for spend in spends:
        temp = {
            'id': spend.id,
            'date': spend.date,
            'price': spend.price,
            'on': spend.on
        }
        spendsJSON.append(temp)
    return jsonify({'spends': spendsJSON})
