from . import db

class order_process(db.Model):
    __tablename__ = 'order_process'
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,unique=True,nullable=False)
    execution_price = db.Column(db.Float, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'execution_price': self.execution_price
            }