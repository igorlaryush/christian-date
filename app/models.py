from app import db, bcrypt
from datetime import datetime
import pytz  # Importing pytz for timezone support


class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swiper_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_like = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Swipe(swiper_id={self.swiper_id}, target_id={self.target_id}, is_like={self.is_like})>"

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f"<Match(user1_id={self.user1_id}, user2_id={self.user2_id})>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    interests = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))
    gender = db.Column(db.String(50), nullable=True)
    
    location_x = db.Column(db.Float, nullable=True)  # X coordinate for preference
    location_y = db.Column(db.Float, nullable=True)  # Y coordinate for preference

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    max_distance_km = db.Column(db.Float, nullable=True)  # Max distance for matching
    interests = db.Column(db.String(255), nullable=False)
    interested_in_confessions = db.Column(db.String(255), nullable=True)
    not_interested_in_confessions = db.Column(db.String(255), nullable=True)
    interested_in_genders = db.Column(db.String(255), nullable=True)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))

    messages = db.relationship('Message', backref='chat', lazy=True)

    def __repr__(self):
        return f"<Chat between user1_id={self.user1_id} and user2_id={self.user2_id}>"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))

    def __repr__(self):
        return f"<Message from user_id={self.sender_id} in chat_id={self.chat_id}>"
