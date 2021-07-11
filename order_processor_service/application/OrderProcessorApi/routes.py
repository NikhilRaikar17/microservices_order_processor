from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import pymysql
from sqlalchemy.sql import func
import random
from . import order_processor_api_blueprint
from .. import db,create_app
from ..models import order_process
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)

@order_processor_api_blueprint.route('/exec_price/<int:id>')
def exec_price(id):
    try:
        connection = pymysql.connect(host='docker.for.mac.localhost',
                                    database='main',
                                    user='root',
                                    password='root',
                                    port=33067)
        cursor=connection.cursor()
        order_id=id
        cursor.execute(f"Select * from orders where order_id={order_id}")
        results=cursor.fetchall()
        for result in results:
            OrderExecutionPrice = result[2]*random.uniform(1.1,2.0)
            print(str(OrderExecutionPrice))
            new_order_processing = order_process(order_id=id,execution_price=OrderExecutionPrice)
            db.session.add(new_order_processing)
            db.session.commit()
            return jsonify({'value':str(OrderExecutionPrice)})
    except Exception as e:
        print("Error while connecting to MySQL", e)
        return ''

@order_processor_api_blueprint.route('/metrics', methods=['GET'])
def metrics():
    total_orders = len(order_process.query.all())
    average = order_process.query.with_entities(func.avg(order_process.execution_price)).all()

    return jsonify({
            'total_orders_processed': total_orders,
            'average':average[0][0]
            })

        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
