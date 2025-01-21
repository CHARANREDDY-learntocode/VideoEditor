from flask import Flask
from routers.video import video_bp
from config import Config
from models import db

from util.auth import authenticate

# Initialize the Flask app and configure it
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the SQLAlchemy instance
db.init_app(app)


# Register the blueprint
app.register_blueprint(video_bp, url_prefix='/video')

@app.route('/')
def home():
    return "Welcome to the Video Processing API!"


@app.before_request
def verify_auth():
    authenticate()

if __name__ == '__main__':
    with app.app_context():
        # Create all tables (if they don't exist)
        db.create_all()
    app.run(debug=True)