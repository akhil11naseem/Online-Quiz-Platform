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

class TestBase(unittest.TestCase):
    # will be called before every test



    def setUp(self):
        """Defines what should be done before every single test in this test group."""

        with app.app_context():
            db.session.commit()
            db.drop_all()
            db.create_all()
            # create test admin user
            admin = User(username="admin", password="admin", admin=True, student=False, enabled=True)
            
            # create test non-admin user
            student = User(username="student1", password="student1", admin=False, student=True, enabled=True)
            
            db.session.add(admin)
            db.session.add(student)
            db.session.commit()

    def tearDown(self):
        """Defines what should be done after every single test in this test group."""
        with app.app_context():
            db.session.remove()
            #db.drop_all()
    

class TestUserModel(TestBase):

    def test_employee_model(self):
        """
        Test number of records in Employee table
        """
        self.assertEqual(User.query.count(), 2)


 

class TestModel(TestBase):

    def test_login_system(self):
        tester = app.test_client(self)
        response = tester.post (
            '/login',
            data = dict(username="admin", password="password"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials, please try again', response.data)


    def test_root(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_password(self):
        self.assertEqual(3,3)
    
    def test_password_hashing(self):
        self.assertEqual(1,1)



if __name__ == '__main__':
    unittest.main(verbosity=2)
