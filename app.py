from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from routes.cart_routes import cart_bp
from routes.product_routes import product_bp
from models import db, init_db

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///levi.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
init_db(app)

# Register Routes
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(product_bp)


# Create Tables Before Running
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
