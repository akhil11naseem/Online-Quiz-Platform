import unittest, os

from flask_app.extensions import db
from flask_app.models import User, Topic, Results
from flask_testing import TestCase
from flask_app.__init__ import create_app

class UserModelTest(unittest.TestCase):
    # will be called before every test
 
    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:://test.db'
        )
        return app

    def tearDown(self):
        db.session.remove()

    def test_set_pw(self):
        u = User.query.get(1)
        u.unhashed_password('pw')
        self.assertFalse(u.unhashed_password('passw0rd'))
        self.assertTrue(u.unhashed_password('pw'))




if __name__ == '__main__':
    unittest.main(verbosity=2)
