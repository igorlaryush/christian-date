import os
import logging
from logging.handlers import RotatingFileHandler

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dating_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'

    # SQLAlchemy echo feature
    SQLALCHEMY_ECHO = True

    # Logging configuration
    LOG_FILE = 'app.log'

    @staticmethod
    def setup_logging(log_file):
        # Open the file in 'write' mode to clear its contents
        with open(log_file, 'w'):
            pass  # This will clear the file without deleting it

        # Set up logging with the RotatingFileHandler
        logging.basicConfig(
            handlers=[RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)],
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Optional: Configure SQLAlchemy logging
        sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
        sqlalchemy_logger.setLevel(logging.INFO)

    # Call the setup function to initialize logging when the app starts
    setup_logging(LOG_FILE)
