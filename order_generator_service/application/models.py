from . import db

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True,unique=True)
    symbol = db.Column(db.String(200))
    quantity = db.Column(db.Integer)

    def to_json(self):
        return {
            'order_id': self.order_id,
            'symbol': self.symbol,
            'quantity': self.quantity
            }