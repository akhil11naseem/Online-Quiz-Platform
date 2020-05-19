from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


import os 

#Create instance of LoginManager
login_manager = LoginManager()

#Create Database Object db
db = SQLAlchemy()

