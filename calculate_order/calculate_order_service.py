from flask import Flask, jsonify, abort
from flask_cors import CORS
import random
import pymysql

app = Flask(__name__)
CORS(app)

@app.route('/exec_price/<int:id>')
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
            return jsonify({'value':str(OrderExecutionPrice)})
    except Exception as e:
        print("Error while connecting to MySQL", e)
        return ''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
