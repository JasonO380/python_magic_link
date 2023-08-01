print("Loading app")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from app.config import active_config

app = Flask(__name__)
app.config.from_object(active_config)
mail = Mail(app)
db= SQLAlchemy(app)
migrate = Migrate(app, db)


# import the models.py classes to create tables
from app import models
#create all tables for database 
with app.app_context():
    db.create_all()

#import routes after flask app is created
from app import routes

