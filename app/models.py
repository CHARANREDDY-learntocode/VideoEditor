from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Float, nullable=False)  # size in MB
    duration = db.Column(db.Float, nullable=False)  # duration in seconds
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    path = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f"<Video {self.filename} ({self.size} MB)>"

class SharedLink(db.Model):
    __tablename__ = 'shared_links'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)

    video = db.relationship('Video', backref=db.backref('shared_links', lazy=True))

    def __repr__(self):
        return f"<SharedLink for Video ID {self.video_id} (Expires at {self.expiry_time})>"
