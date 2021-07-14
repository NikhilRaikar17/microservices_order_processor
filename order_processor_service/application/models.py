from . import db

class order_process(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,unique=True)
    execution_price = db.Column(db.Float)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'execution_price': self.execution_price
            }