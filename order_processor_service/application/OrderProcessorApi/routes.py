from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from sqlalchemy.sql import func
import random
from . import order_processor_api_blueprint
from .. import db,create_app
from ..models import order_process
from flask_sqlalchemy import SQLAlchemy
from .api.OrderInfo import OrderInfoClient

app = create_app()
db = SQLAlchemy(app)

@order_processor_api_blueprint.route('/cal_execution_price/<int:id>',methods=['GET','POST'])
def cal_execution_price(id):
    try:
        response = OrderInfoClient.get_info(id)
        quantity = int(response['quantity'])
        OrderExecutionPrice = quantity*random.uniform(1.1,2.0)
        print(str(OrderExecutionPrice))
        new_order_processing = order_process(order_id=id,execution_price=OrderExecutionPrice)
        db.session.add(new_order_processing)
        db.session.commit()
        return jsonify({'value':str(OrderExecutionPrice)})
    except Exception as e:
        print("Error while connecting to MySQL", e)
        return jsonify({'ERROR': e})

@order_processor_api_blueprint.route('/metrics', methods=['GET'])
def metrics():
    total_orders = len(order_process.query.all())
    average = order_process.query.with_entities(func.avg(order_process.execution_price)).all()
    total_average = average[0][0]
    return jsonify({
            'TotalOrdersProcessed': total_orders,
            'AverageOrderExecutionPrice':total_average
            })

        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
