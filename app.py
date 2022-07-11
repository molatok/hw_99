
import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        user_data = User.query.all()
        return json.dumps([user.to_dict() for user in user_data])
    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return "Пользователь создан", 200


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Нет такого"
        else:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Нет такого", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age'],
        user.email = user_data['email'],
        user.role = user_data['role'],
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f'Объект с id {user_id} изменен', 200
    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return 'Пользователь не найден', 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f'Объект с id {user_id} удален', 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        order_data = Order.query.all()
        return jsonify([order.to_dict() for order in order_data])
    if request.method == 'POST':
        order = json.loads(request.data)
        month_start, day_start, year_start = [int(o) for o in order['start_date'].split('/')]
        month_end, day_end, year_end = order['end_date'].split('/')
        new_order = Order(
            d=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=year_start, month=month_start, day=day_start),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()
        db.session.close()
        return "Заказ создан", 200
    
    
@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Нет такого"
        else:
            return jsonify(order.to_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Нет такого", 404
        order.name = order_data['first_name']
        order.description = order_data['last_name']
        order.start_date = order_data['age'],
        order.end_date = order_data['email'],
        order.address = order_data['role'],
        order.price = order_data['phone']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f'Объект с id {order_id} изменен', 200
    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return 'Заказ не найден', 404
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f'Объект с id {order_id} удален', 200


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        offer_data = Offer.query.all()
        return json.dumps([offer.to_dict() for offer in offer_data])
    if request.method == 'POST':
        offer = json.loads(request.data)
        new_offer = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer)
        db.session.commit()
        db.session.close()
        return "Предложение создано", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Нет такого"
        else:
            return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(User).get(offer_id)
        if offer is None:
            return "Нет такого", 404
        offer.order_id = offer_data['order_id']
        offer.last_name = offer_data['executor_id']
        return f'Объект с id {offer_id} изменен', 200
    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return 'Предложение не найдено', 404
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f'Предложение с id {offer_id} удалено', 200
       
        
if __name__ == '__main__':
    app.run()
