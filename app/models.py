from sqlalchemy.sql import func
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.Column(db.JSON)
    authenticated = db.Column(db.Boolean, default=False)
    login_token = db.Column(db.String(120), unique=True, nullable=True)
    token_expiry = db.Column(db.DateTime, nullable = True)
    user_created = db.Column(db.DateTime, nullable=False)
    user_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

