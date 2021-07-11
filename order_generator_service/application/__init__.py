from flask import Flask
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
    CORS(app)    
    db.init_app(app)
    with app.app_context():
        from .ordersapi import orders_api_blueprint
        app.register_blueprint(orders_api_blueprint)
        return app
    