import random
from . import orders_api_blueprint
from .. import db,scheduler,create_app
from ..models import orders
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

def generate_orders():
    new_order = orders(symbol='AAP', quantity=random.randint(1,10))
    print(db)
    db.session.add(new_order)
    try:
        db.session.commit()
        order_id = new_order.order_id
        publish(body=f"{order_id}")

        return {
                'order_number':order_id
                }

    except Exception as e:
        print(e)
        db.session.rollback()
        db.session.flush()
        return {
                'message':'Orders not processed',
                'Error':e
                }