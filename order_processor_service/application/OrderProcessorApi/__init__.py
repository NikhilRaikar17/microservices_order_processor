from flask import Blueprint

order_processor_api_blueprint = Blueprint('order_processor_api', __name__)

from . import routes