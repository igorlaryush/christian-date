from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO()  # Add this line to initialize the SocketIO instance

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")  # Initialize SocketIO with the app and allow all CORS origins
    
    from .routes import (
        auth_routes,
        chat_routes,
        message_routes,
        preference_routes,
        swipe_routes,
        user_routes,
    )
    
    app.register_blueprint(user_routes.bp, url_prefix='/user_routes')
    app.register_blueprint(preference_routes.bp, url_prefix='/prefs')
    app.register_blueprint(chat_routes.bp, url_prefix='/chats')
    app.register_blueprint(message_routes.bp, url_prefix='/messages')
    app.register_blueprint(auth_routes.bp, url_prefix='/auth')
    app.register_blueprint(swipe_routes.bp, url_prefix='/swipe')

    return app