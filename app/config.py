import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Use your preferred database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    SECRET_KEY = os.urandom(24)  # Random secret key for sessions and CSRF protection