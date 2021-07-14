import random,string
from . import orders_api_blueprint
from .. import db,scheduler,create_app
from ..models import Orders
from .producer import publish
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)


@orders_api_blueprint.route('/')
def index():
    scheduler.add_job(func=generate_orders, trigger="interval", seconds=2)
    return {
            'message':'Orders are executed every two seconds'
            }

def get_symbol(size=3, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_orders():
    symbol = get_symbol()
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
    order = Orders.query.filter_by(order_id=id).first()
    return {'quantity':order.quantity}

@orders_api_blueprint.route('/stop_orders', methods=['GET'])
def stop_orders():
    scheduler.shutdown(wait=False)
    return {'message':'Stopping processing orders'}
