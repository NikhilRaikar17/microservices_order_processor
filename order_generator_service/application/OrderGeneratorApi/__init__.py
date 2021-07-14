from flask import Blueprint

orders_api_blueprint = Blueprint('orders_api', __name__)

from . import routes