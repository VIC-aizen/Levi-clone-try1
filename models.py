from flask_sqlalchemy import SQLAlchemy
import datetime  # Import datetime module

db = SQLAlchemy()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy instance

def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed password
    email = db.Column(db.String(100), unique=True, nullable=False)

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed password
    email = db.Column(db.String(100), unique=True, nullable=False)


# Products Table
class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)

# Cart Table
class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Products', backref=db.backref('cart_items', lazy=True))
# Orders Table
class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")

# Order Items Table
class OrderItems(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Products', backref='order_items', lazy=True)  # Relationship to get product details
# Payments Table
class Payments(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Example: "Success" / "Failed" / "Pending"
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) 
    # Relationships
    order = db.relationship('Orders', backref=db.backref('payments', lazy=True))
    user = db.relationship('Users', backref=db.backref('payments', lazy=True))

    def __init__(self, order_id, user_id, amount, payment_method, status, date=None):
        self.order_id = order_id
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
        self.date = date if date else datetime.datetime.now()

# Returns Table
class Returns(db.Model):
    __tablename__ = 'returns'
    return_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")

# Sales Table
class Sales(db.Model):
    __tablename__ = 'sales'

    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Relationships (Optional: Helps in accessing related data easily)
    product = db.relationship('Products', backref=db.backref('sales', lazy=True))
    order = db.relationship('Orders', backref=db.backref('sales', lazy=True))
    user = db.relationship('Users', backref=db.backref('sales', lazy=True))

    def __init__(self, product_id, quantity_sold, total_revenue, order_id, user_id):
        self.product_id = product_id
        self.quantity_sold = quantity_sold
        self.total_revenue = total_revenue
        self.order_id = order_id
        self.user_id = user_id


# Shipping Table
class Shipping(db.Model):
    __tablename__ = 'shipping'
    shipping_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Processing")

# Stocks Table
class Stocks(db.Model):
    __tablename__ = 'stocks'
    stock_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Suppliers Table
class Suppliers(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
