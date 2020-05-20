import unittest, os

from ..extensions import db
from ..commands import create_tables
from ..models import User, Topic, Results
from flask_testing import TestCase
from .. import create_app

class UserModelTest(unittest.TestCase):
    # will be called before every test

    def setUp(self):
        """Defines what should be done before every single test in this test group."""

        app=create_app(config_file='test_settings.py')

        self.app = app.test_client()

        # create test admin user
        admin = User(username="admin", password="admin", admin=True, student=False, enabled=True)

        # create test non-admin user
        student = User(username="student1", password="student1", admin=False, student=True, enabled=True)

        with app.app_context():
            db.create_all()
            db.session.add(admin)
            db.session.add(student)
            db.session.commit()


    def tearDown(self):
        """Defines what should be done after every single test in this test group."""
        # db.session.remove()
        # db.drop_all()

    def test_password_hashing(self):
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
