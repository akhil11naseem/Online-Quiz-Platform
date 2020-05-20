import unittest, os

from ..extensions import db
from ..models import User, Topic, Results
from flask_testing import TestCase
from .. import create_app

class UserModelTest(unittest.TestCase):
    # will be called before every test

    def create_app(self):
        app = create_app(config_file='test_settings.py')
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = User(username="admin", password="admin", admin="True", student="False", enabled="True")

        # create test non-admin user
        student = User(username="student1", password="student1", admin="False", student="True", enabled="True")

        # save users to database
        db.session.add(admin)
        db.session.add(student)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_set_pw(self):
        u = User.query.get(1)
        u.unhashed_password('pw')
        self.assertFalse(u.unhashed_password('passw0rd'))
        self.assertTrue(u.unhashed_password('pw'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
