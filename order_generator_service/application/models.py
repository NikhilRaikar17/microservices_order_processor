from . import db

class Orders(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    symbol = db.Column(db.String(200),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)

    def to_json(self):
        return {
            'order_id': self.order_id,
            'symbol': self.symbol,
            'quantity': self.quantity
            }