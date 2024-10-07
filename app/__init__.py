from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from flask_mail import Mail

app = Flask(__name__, template_folder="../templates")  # Explicitly specify the template folder

app.config.from_object('config.Config')
mongo = PyMongo(app)
mail = Mail(app)

from app import routes
