import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///tests/db_testing.sqlite3'
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
