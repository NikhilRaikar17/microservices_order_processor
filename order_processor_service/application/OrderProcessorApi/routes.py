from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from . import order_processor_api_blueprint
from .. import db,create_app
from flask_sqlalchemy import SQLAlchemy
from ..models import order_process
from sqlalchemy.sql import func
import random
from .api.OrderInfo import OrderInfoClient

app = create_app()
db = SQLAlchemy(app)

@order_processor_api_blueprint.route('/cal_execution_price/<int:id>',methods=['GET','POST'])
def cal_execution_price(id):
    """Order execution price is calculated for each processing order"""
    try:
        if not id:
            raise Exception('Invalid ID passed')
        
        response = OrderInfoClient.get_info(id)
        if not response['quantity']:
            raise Exception('Quantity for this order number is None')
        
        quantity = int(response['quantity'])
        OrderExecutionPrice = quantity*random.uniform(1.1,2.0)

        print(str(OrderExecutionPrice))
        
        new_order_processing = order_process(order_id=id,execution_price=OrderExecutionPrice)
        db.session.add(new_order_processing)
        try:
            db.session.commit()
            print('successfully added the execution price or order_id:',new_order_processing.id)
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            raise Exception('Cannot add the execution price to database, order_id',id)

        return jsonify({'value':str(OrderExecutionPrice)})

    except Exception as e:
        message = e.args[0]
        return jsonify({'ERROR': message})

@order_processor_api_blueprint.route('/metrics', methods=['GET'])
def metrics():
    """ Calculates the number of orders processed 
        and average execution price"""
    try:
        total_orders = len(order_process.query.all())

        if total_orders < 1:
            raise Exception('No processed orders in the database yet')
        
        average = order_process.query.with_entities(func.avg(order_process.execution_price)).all()
        total_average = average[0][0]
        return jsonify({
                'TotalOrdersProcessed': total_orders,
                'AverageOrderExecutionPrice':total_average
                })
                
    except Exception as e:
        message = e.args[0]
        return jsonify({'ERROR':message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
