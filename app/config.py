import os
from dotenv import load_dotenv
import secrets
# Fetch the environment
ENV = os.getenv("FLASK_ENV", "development")
# load the env files
load_dotenv()
# create a random token
token=secrets.token_hex(8)

# Set the configurations
class Config:
    # Set up SQLAlchemy configurations
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # Set up Flask-Mail configurations
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAGIC_KEY = token
    # Secret key for signing tokens
    SECRET_KEY = os.getenv("SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Use a dictionary to map the configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

# Set the active config
active_config = config.get(ENV, DevelopmentConfig)