from flask import Blueprint

admin_routes = Blueprint('admin_routes', __name__)
user_routes = Blueprint('auth_routes', __name__)
cart_routes = Blueprint('cart_routes', __name__)
order_routes = Blueprint('order_routes', __name__)
product_routes = Blueprint('product_routes', __name__)

from . import admin_routes, cart_routes, order_routes, product_routes, user_routes
