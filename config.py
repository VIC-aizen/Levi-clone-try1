import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///levi.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
