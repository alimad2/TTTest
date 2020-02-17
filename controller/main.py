from flask import Blueprint, request, abort, jsonify, url_for

import service.service as service

blue = Blueprint('test', __name__)


class Spss():
    def __init__(self, price, date, category):
        self.price = price
        self.date = date
        self.category = category


@blue.route('/spends', methods=['GET'])
def get_all():
    price = request.args.get('price')
    date = request.args.get('date')
    page = request.args.get('page')
    per_page = request.args.get('pp')
    category = request.args.get('category')

    spends = service.get_all(price, date, page, category, per_page)
    spendsJSON = []

    for spend in spends:
        temp = {
            'id': spend.id,
            'date': spend.date,
            'price': spend.price,
            'category': spend.category.name,
            'url': url_for('test.get_spend', spend_id=spend.id, _external=True)
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
        'category': spend.category.name,
    }
    return jsonify({'spend': spendjson})


@blue.route('/spends', methods=['POST'])
def new_spend():
    if not request.json:
        abort(400)
    spend = {
        'date': request.json['date'],
        'price': request.json['price'],
        'category': request.json['category'],
    }
    spend = service.create_spend(spend)
    if spend == False:
        abort(400)
    spendjson = {
        'id': spend.id,
        'date': spend.date,
        'price': spend.price,
        'category': spend.category.name,
    }
    return jsonify({'spend': spendjson})


@blue.route('/spends/<int:spend_id>', methods=['PUT'])
def update_spend(spend_id):
    sp = Spss(request.json.get('price', 'nothing'), request.json.get('date', 'nothing'),
              request.json.get('category', 'nothing'))
    ret = service.update_spend(spend_id, sp)
    if ret == False:
        abort(404)
    spend = {
        'id': ret.id,
        'date': ret.date,
        'price': ret.price,
        'category': ret.category.name
    }
    return jsonify({'spend': spend})


@blue.route('/spends/<int:spend_id>', methods=['DELETE'])
def delete_spend(spend_id):
    ret = service.delete_spend(spend_id)
    if ret == False:
        abort(404)
    return jsonify({'result': True})


@blue.route('/categories', methods=['GET'])
def get_all_categories():
    categories = service.get_all_categories()
    categoriesJSON = []
    for category in categories:
        temp = {
            'name': category.name,
            'description': category.description
        }
        categoriesJSON.append(temp)
    return jsonify({'categories': categoriesJSON})


@blue.route('/categories', methods=['POST'])
def create_new_category():
    if not request.json:
        abort(400)

    name = request.json.get('name')
    description = request.json.get('description', 'no description')
    category = {
        'name': name,
        'description': description
    }
    category = service.create_category(category)
    categoryJSON = {
        'name': category.name,
        'description': category.description
    }
    return jsonify({'category': categoryJSON})
