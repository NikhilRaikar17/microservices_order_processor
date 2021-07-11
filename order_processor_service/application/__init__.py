from flask import Flask
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
    CORS(app)    
    db.init_app(app)
    with app.app_context():
        from .OrderProcessorApi import order_processor_api_blueprint
        app.register_blueprint(order_processor_api_blueprint)
        return app
    