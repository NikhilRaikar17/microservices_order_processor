from producer import publish
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random,time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

class orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(200))
    quantity = db.Column(db.Integer)

@app.route('/')
def index():
    for each in range(0,10):
        time.sleep(2)
        new_order = orders(symbol='AAP', quantity=random.randint(1,10))
        db.session.add(new_order)
        try:
            db.session.commit()
            order_id = new_order.order_id
            publish(body=f"{order_id}")
            
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            return 'New order cannot be added'
    
    return "Added all 10 items"
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
