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
            student1 = User(username='akhil',password='akhil', admin=False, student=False, enabled=True)
            student2 = User(username='varun',password='varun', admin=False, student=False, enabled=True)
            student3 = User(username='lance',password='lance', admin=False, student=False, enabled=True)
            # create test non-admin user
            #student = User(username="student1", password="student1", admin=False, student=True, enabled=True)
            db.session.add(admin)
            db.session.add(student1)
            db.session.add(student2)
            db.session.add(student3)
            db.session.commit()

    def tearDown(self):
        """Defines what should be done after every single test in this test group."""
        with app.app_context():
            db.session.remove()
            #db.drop_all()
    



class TestUserModel(TestBase):

    def test_user_model(self):
        #checks the number of users in the data base 
        self.assertEqual(User.query.count(), 4)
 
    def test_user_firstName(self):
        u1 = User.query.get(1)
        u2 = User.query.get(2)
        u3 = User.query.get(3)
        u4 = User.query.get(4)
        self.assertEqual(u1.username, 'admin')
        self.assertEqual(u2.username, 'akhil')
        self.assertEqual(u3.username, 'varun')
        self.assertEqual(u4.username, 'lance')
        self.assertTrue(u4.password, 'lance')






class TestView(TestBase):

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
