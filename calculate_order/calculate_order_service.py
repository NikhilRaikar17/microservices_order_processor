#from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests,random
#from producer import publish
import pymysql

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    try:
        connection = pymysql.connect(host='db',
                                    database='main',
                                    user='root',
                                    password='root')
        cursor=connection.cursor()
        order_id=1
        cursor.execute(f"Select * from orders where order_id={order_id}")
        results=cursor.fetchall()
        for result in results:
            OrderExecutionPrice = result[2]*random.uniform(1.1,2.0)
            print (OrderExecutionPrice)
    except Exception as e:
        print("Error while connecting to MySQL", e)
    
    return f'Hello I am calculating'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
