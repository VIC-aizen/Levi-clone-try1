from flask import Blueprint, render_template, request, redirect, url_for
from models import Products  # Assuming Products model is defined in models.py


product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def view_products():
    products = Products.query.all()
    return render_template('products.html', products=products)
