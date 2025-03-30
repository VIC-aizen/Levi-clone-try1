from models import db, Admin
from hashpass import hash_password
from app import app  # Import app to use db

# Create a new admin
with app.app_context():
    admin_username = "admin"
    admin_password = "admin123"
    admin_email = "admin@example.com"

    hashed_pw = hash_password(admin_password)  # Hash password before saving

    new_admin = Admin(username=admin_username, password=hashed_pw, email=admin_email)
    db.session.add(new_admin)
    db.session.commit()

    print("Admin created successfully!")
