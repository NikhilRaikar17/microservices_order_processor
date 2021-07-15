from . import orders_api_blueprint
from .. import db,scheduler,create_app
from flask_sqlalchemy import SQLAlchemy
from .producer import publish
import random,string
from ..models import Orders

app = create_app()
db = SQLAlchemy(app)


@orders_api_blueprint.route('/')
def index():
    scheduler.add_job(func=generate_orders, trigger="interval", seconds=2)
    return {
            'message':'Orders are executed every two seconds'
            }

def get_symbol(size=3, chars=string.ascii_uppercase + string.digits):
    """ Generate random string of three characters long which 
    is regarded as a symbol"""
    return ''.join(random.choice(chars) for _ in range(size))

def generate_orders():
    """ Generates orders """
    symbol = get_symbol()
    if len(symbol) < 3 or len(symbol) > 3:
        raise Exception('Symbol length is less than or greater than 3, it should be 3')
        
    new_order = Orders(symbol=symbol, quantity=random.randint(1,10))
    db.session.add(new_order)
    try:
        db.session.commit()
        order_id = new_order.order_id
        publish(body=f"{order_id}")
        print(f"Order number {order_id} processed")
    except Exception as e:
        print(e)
        db.session.rollback()
        db.session.flush()
        return {
                'message':'Orders not processed',
                'Error':e
                }

@orders_api_blueprint.route('/order_info/<int:id>', methods=['GET'])
def get_order_info(id):
    """ Gets information regarding an order, in our case it
    returns the quantity of that order"""
    try:

        if not type(id) is int:
            raise Exception('Invalid order_id passed')

        order = Orders.query.filter_by(order_id=id).first()
        if not order:
            raise Exception('No orders found for the sent order_id')

        return {'quantity':order.quantity}
    except Exception as e:
        message = e.args[0]
        print(message)
        return {'quantity':None}

@orders_api_blueprint.route('/stop_orders', methods=['GET'])
def stop_orders():
    scheduler.shutdown(wait=False)
    return {'message':'Stopping processing orders'}