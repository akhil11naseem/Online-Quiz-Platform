import unittest, os
from ..extensions import db
from ..commands import create_tables
from ..models import User, Topic, Results
from flask_testing import TestCase
from .. import create_app
from flask import url_for
from flask import Flask
from flask_login import current_user
app = Flask(__name__)
app=create_app(config_file='test_settings.py')
app.testing = True
app.test_client()

class TestBase(unittest.TestCase):

    def create_app(self):
        app=create_app(config_file='test_settings.py')
        return app
    # will be called before every test
    def setUp(self):
        """Defines what should be done before every single test in this test group."""

        with app.app_context():
            #db.session.query(User).delete()
            db.session.commit()
            db.drop_all()
            db.create_all()
            # create test admin user
            admin = User(username="admin", password="admin", admin=True, student=False, enabled=True)
            self.student1 = User(username='akhil',password='akhil', admin=False, student=False, enabled=True)
            self.student2 = User(username='varun',password='varun', admin=False, student=False, enabled=True)
            student3 = User(username='lance',password='lance', admin=False, student=False, enabled=True)
            db.session.add(admin)
            db.session.add(self.student1)
            db.session.add(self.student2)
            db.session.add(student3)
<<<<<<< HEAD
            db.session.commit()
            u1 = User.query.get(1)
            u2 = User.query.get(2)
            self.assertEqual(u1.username, 'admin')
            self.assertEqual(u2.username, 'akhil')

            topic1 = Topic(name='english', questions = '...', enabled = True)
            topic2 = Topic(name='maths', questions = 'abs', enabled = False)
            db.session.add(topic1)
            db.session.add(topic2)
            db.session.commit()
            results1 = Results(score='123', result_of_user_id='456', result_for_topic_id='789')
            db.session.add(results1)

=======
            db.session.commit()
            u1 = User.query.get(1)
            u2 = User.query.get(2)
            self.assertEqual(u1.username, 'admin')
            self.assertEqual(u2.username, 'akhil')

            topic1 = Topic(name='english', questions = '...', enabled = True)
            topic2 = Topic(name='maths', questions = 'abs', enabled = False)
            db.session.add(topic1)
            db.session.add(topic2)
            db.session.commit()
            results1 = Results(score='123', result_of_user_id='456', result_for_topic_id='789')
            db.session.add(results1)
           
>>>>>>> origin/master
            # create test non-admin user
            #student = User(username="student1", password="student1", admin=False, student=True, enabled=True)
            db.session.commit()

    def tearDown(self):
        """Defines what should be done after every single test in this test group."""
        with app.app_context():
            db.session.remove()
            #db.drop_all()


class TestUserModel(TestBase):
    def test_login_page(self):
        tester = app.test_client()
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_registeration_page(self):
        tester = app.test_client(self)
        response = tester.post (
            '/register',
            data = dict(username="julie", password="julie"),
            follow_redirects=True
        )

    #Ensure the correct user is logged in
    def test_logout(self):
        tester = app.test_client(self)
        with app.app_context():
            response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
<<<<<<< HEAD


    def test_incorrect_login(self):
        tester = app.test_client(self)
        with app.app_context():
            response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials, please try again.', response.data)


    '''

class TestUserModel(TestBase):

    def test_topic_model(self):
        topic2 = Topic(name='maths', questions= 'abs', enabled = True)
        topic3 = Topic(name='math', questions= 'absx', enabled = True)
        db.session.add(topic2)
        db.session.add(topic3)
        db.session.commit()



    def test_user_model(self):

        self.student1 = User(username='akhil',password='akhil', admin=False, student=False, enabled=True)
        self.student2 = User(username='varun',password='varun', admin=False, student=False, enabled=True)
        student3 = User(username='lance',password='lance', admin=False, student=False, enabled=True)
        db.session.add(self.student1)
        db.session.add(self.student2)
        db.session.add(student3)
        db.session.commit()
        u1 = User.query.get(1)
        u2 = User.query.get(2)
        self.assertEqual(u1.username, 'admin')
        self.assertEqual(u2.username, 'akhil')
        #checks the number of users in the data base
        self.assertEqual(User.query.count(), 4)


   '''



class TestModel(TestBase):

    def test_login_system(self):
        tester = app.test_client(self)
        response = tester.post (
            '/login',
            data = dict(username="admin", password="password"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials, please try again', response.data)

    def test_register_and_login(self):
        # register a new account
        tester = app.test_client()
        response = tester.post(url_for('auth.register'), data={
            'username': 'john',
            'password': 'cat',
        })
        self.assertTrue(response.status_code == 302)

    def test_root(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_root_login(self):
        tester = app.test_client()
        response = tester.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_password(self):
        self.assertEqual(3,3)
=======
>>>>>>> origin/master


    def test_incorrect_login(self):
        tester = app.test_client(self)
        with app.app_context():
            response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials, please try again.', response.data)


    '''

class TestUserModel(TestBase):

    def test_topic_model(self):
        topic2 = Topic(name='maths', questions= 'abs', enabled = True)
        topic3 = Topic(name='math', questions= 'absx', enabled = True)
        db.session.add(topic2)
        db.session.add(topic3)
        db.session.commit()



    def test_user_model(self):
        
        self.student1 = User(username='akhil',password='akhil', admin=False, student=False, enabled=True)
        self.student2 = User(username='varun',password='varun', admin=False, student=False, enabled=True)
        student3 = User(username='lance',password='lance', admin=False, student=False, enabled=True)
        db.session.add(self.student1)
        db.session.add(self.student2)
        db.session.add(student3)
        db.session.commit()
        u1 = User.query.get(1)
        u2 = User.query.get(2)
        self.assertEqual(u1.username, 'admin')
        self.assertEqual(u2.username, 'akhil')
        #checks the number of users in the data base 
        self.assertEqual(User.query.count(), 4)


   '''



class TestModel(TestBase):

    def test_login_system(self):
        tester = app.test_client(self)
        response = tester.post (
            '/login',
            data = dict(username="admin", password="password"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials, please try again', response.data)

    def test_register_and_login(self):
        # register a new account
        tester = app.test_client()
        response = tester.post(url_for('auth.register'), data={
            'username': 'john',
            'password': 'cat',
        })
        self.assertTrue(response.status_code == 302)
            
    def test_root(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_root_login(self):
        tester = app.test_client()
        response = tester.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_password(self):
        self.assertEqual(3,3)
    
    def test_password_hashing(self):
        self.assertEqual(1,1)



if __name__ == '__main__':
    unittest.main(verbosity=2)
