import unittest, os
from ..extensions import db
from ..commands import create_tables
from ..models import User, Topic, Results
from flask_testing import TestCase
from .. import create_app
from flask import url_for


app=create_app(config_file='test_settings.py')
app.testing = True
app.test_client()

class BaseCase(unittest.TestCase):
    # will be called before every test
    def setUp(self):
        """Defines what should be done before every single test in this test group."""

        with app.app_context():
            db.session.commit()
            db.drop_all()
            db.create_all()
            # create test admin user
            admin = User(score='123', esult_of_user_id = '456', admin=True, student=False, enabled=True)
            # create test non-admin user
            #student = User(username="student1", password="student1", admin=False, student=True, enabled=True)
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        """Defines what should be done after every single test in this test group."""
        with app.app_context():
            db.session.remove()
            #db.drop_all()