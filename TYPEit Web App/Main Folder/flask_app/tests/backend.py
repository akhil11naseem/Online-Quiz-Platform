import unittest, os
from ..extensions import db
from ..commands import create_tables
from ..models import User, Topic, Results
from flask_testing import TestCase
from .. import create_app
from flask import url_for
from flask import Flask
from flask import request
from urllib.parse import urlparse
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash


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
            admin = User(username="admin", password=generate_password_hash("admin"), admin=True, student=False, enabled=True)
            self.student1 = User(username='akhil',password=generate_password_hash('akhil'), admin=False, student=True, enabled=True)
            self.student2 = User(username='varun',password='varun', admin=False, student=False, enabled=True)
            student3 = User(username='lance',password='lance', admin=False, student=False, enabled=True)
            db.session.add(admin)
            db.session.add(self.student1)
            db.session.add(self.student2)
            db.session.add(student3)
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
           
            # create test non-admin user
            #student = User(username="student1", password="student1", admin=False, student=True, enabled=True)
            db.session.commit()

    def tearDown(self):
        """Defines what should be done after every single test in this test group."""
        with app.app_context():
            db.session.remove()
            #db.drop_all()
'''
    def test_logout(self):
        tester = app.test_client(self)
        #user = User.query.filter_by(id=current_user.id).all()[0]
        with app.app_context():
            response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True)
            data = response.get_data(as_text=True)
            self.assertIn(b'Welcome to Flask!', response.data)
'''


class UserLoginModel(TestBase):

    #Ensure Flask is setup correctly 
    def test_login_index(self):
        tester = app.test_client()
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    #Ensure the choose-test-topic page requires user login
    def test_choose_test_topic_login(self):
        tester = app.test_client()
        response = tester.get('/login', follow_redirects=True)
        self.assertIn(b'Log in', response.data)

    #Feed incorrect credentials to login 
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="lambo", 
            password="lambo"), 
            follow_redirects=True
        )
        self.assertNotIn(b'invalid details, try again.', response.data)
        self.assertIn(b'Invalid credentials, please try again.', response.data)
        

    #Ensure that the currently logged user can logout
    def test_logging_out(self):
        tester = app.test_client(self)
        responsee = tester.post(
            '/login',
            data=dict(username="admin", 
            password="admin"), 
            follow_redirects=True,
            #print(request.endpoint)
        )
        
        self.assertEqual(responsee.status_code, 200)
        #print(responsee.data)
        response = tester.get('/logout', follow_redirects=True)
        #print(response.data)
        #self.assertIn(b'Please log  in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are now logged out', response.data)
        #print(response.data)
        #https://developpaper.com/configuration-tutorial-of-server_name-domain-name-item-in-pythons-flask-framework/
        #assert url_for("logout", _external=False) in page
        #self.assertIn(b'You are now logged out', response.data)
        #check if the user is logged out or still active


    #Ensure log in behaves correclty when fed with user data
    def test_login(self):
       
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = dict(username='akhil', password='akhil'),
            follow_redirects = True
        )
        self.assertIn(b'Choose test topic', response.data)

#--------------- Students Login Page ---------------------------#

    #check if the correct password is given after unhashing 


    #make sure that the logout page requires the user to be logged 
    #checks if the admin is logged in, and from that check if the admin can go back to the log in page
    def test_check_admin_logging_out(self):
        tester = app.test_client(self)
        responsee = tester.post(
            '/login',
            data=dict(username="admin", 
            password="admin"), 
            follow_redirects=True,
            #print(request.endpoint)
        )
        
        self.assertEqual(responsee.status_code, 200)
        #print(responsee.data)

        response = tester.get('/logout', follow_redirects=True)
        #print(response.data)
        #self.assertIn(b'Please log  in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are now logged out', response.data)

    #check if the student is logged in, and from that check if the student can go back to the log in pge
    #/select-topics
    #/manage-students
    #/class-scores
    def test_check_admin_check_pages(self):
        
        tester = app.test_client(self)
        responsedd = tester.post(
            '/login',
            data=dict(username='admin', 
            password='admin'), 
            follow_redirects=True,
            #print(request.endpoint)
        )
        self.assertEqual(responsedd.status_code, 200)
        #print(responsedd.data)
        #checks choose-test-topic page works
        response_Select_Topics = tester.get('/select-topics', follow_redirects=True)
        self.assertIn(b'Welcome, Admin!', response_Select_Topics.data)
        self.assertIn(b'Toggle topics for students', response_Select_Topics.data)
        
        #response_Test_Topics = tester.get('/logout', follow_redirects=True)
        #response_Change_Password = tester.get('/logout', follow_redirects=True)


        #checks my-score page works
        response_Class_Score = tester.get('/class-scores', follow_redirects=True)
        #print(response_Class_Score.data)
        self.assertIn(b'Welcome, Admin!', response_Class_Score.data)
        self.assertIn(b'Class scores', response_Class_Score.data)
        self.assertIn(b'Student', response_Class_Score.data)
        #self.assertIn(b'Class top score', response_My_Scores.data)


        #self.assertIn(b'Choose test topic', response_Settings.data)
        #self.assertIn(b'Welcome, akhil!', response_Settings.data)
        #response_Test_Topics = tester.get('/logout', follow_redirects=True)
        #response_Change_Password = tester.get('/logout', follow_redirects=True)
        
        
        response_Manage_Students = tester.get('/manage-students', follow_redirects=True)
        #print(response_My_Scores.data)
        self.assertIn(b'Welcome, Admin!', response_Manage_Students .data)
        self.assertIn(b'Manage students', response_Manage_Students .data)
        self.assertIn(b'Students', response_Manage_Students .data)
        self.assertIn(b'Enable/Disable', response_Manage_Students .data)
        #self.assertIn(b'Class top score', response_My_Scores.data)
        #response_Welcome = tester.get('/logout', follow_redirects=True)
            #response = tester.get('/logout', follow_redirects=True)
            #print(response.data)
            #self.assertIn(b'Please log  in', response.data)
            #self.assertEqual(response.status_code, 200)
            #self.assertIn(b'You are now logged out', response.data)


    def test_check_student_logging_out(self):
        
        tester = app.test_client(self)
        responsed = tester.post(
            '/login',
            data=dict(username='akhil', 
            password='akhil'), 
            follow_redirects=True,
            #print(request.endpoint)
        )
        self.assertEqual(responsed.status_code, 200)
        #print(responsed.data)

        response = tester.get('/logout', follow_redirects=True)
        #print(response.data)
        #self.assertIn(b'Please log  in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are now logged out', response.data)


  


    #check once the user is logged in, it can access all the pages 

    def test_check_student_check_pages(self):
        
        tester = app.test_client(self)
        responsedd = tester.post(
            '/login',
            data=dict(username='akhil', 
            password='akhil'), 
            follow_redirects=True,
            #print(request.endpoint)
        )
        self.assertEqual(responsedd.status_code, 200)
        #print(responsedd.data)
        #checks choose-test-topic page works
        response_Settings = tester.get('/choose-test-topic', follow_redirects=True)
        self.assertIn(b'Choose test topic', response_Settings.data)
        self.assertIn(b'Welcome, akhil!', response_Settings.data)
        #response_Test_Topics = tester.get('/logout', follow_redirects=True)
        #response_Change_Password = tester.get('/logout', follow_redirects=True)

        #self.assertRedirects(responseClient, redirect_url)


        #checks my-score page works
        response_My_Scores = tester.get('/my-scores', follow_redirects=True)
        #print(response_My_Scores.data)
        #self.assertEqual(response_My_Scores.status_code, 302)
        self.assertIn(b'My scores', response_My_Scores.data)
        self.assertIn(b'Topic', response_My_Scores.data)
        self.assertIn(b'Best score', response_My_Scores.data)
        self.assertIn(b'Class top score', response_My_Scores.data)
        #self.assertIn(b'Choose test topic', response_Settings.data)
        #self.assertIn(b'Welcome, akhil!', response_Settings.data)
        #response_Test_Topics = tester.get('/logout', follow_redirects=True)
        #response_Change_Password = tester.get('/logout', follow_redirects=True)

        #response_Welcome = tester.get('/logout', follow_redirects=True)
            #response = tester.get('/logout', follow_redirects=True)
            #print(response.data)
            #self.assertIn(b'Please log  in', response.data)
            #self.assertEqual(response.status_code, 200)
            #self.assertIn(b'You are now logged out', response.data)

    #check if the correct user is logged in
    
        tester = app.test_client(self)
        target_url = '/logout'
        redirect_url = '/login'
        responseClient = tester.get(target_url)
        self.assertEqual(responseClient.status_code, 401)

    #check when the user is logged in, it can access the tests topic and My scores 


    #check login and register 


    #once you are logged, you shoudl not be able to go to the login or register page


    #registration users with the same user name should not be allowed 

#--------------- Admin Login Page ---------------------------#





#--------------- Registration ---------------------------#

class UserRegisterationModel(TestBase):
    #Check New User can be registered 
    def test_register_index(self):
        tester = app.test_client()
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
#print(response.data)


#Check each New User added to the data base is unquie











#Check the registration page can switch to login page 







'''











#class TestUserModel(TestBase):






    def test_registeration_page(self):
        tester = app.test_client(self)
        response = tester.post (
            url_for('/register'),
            data = dict(username="julie", password="julie"),
            follow_redirects=True
        )
        self.assertEqual(b'Log in', response.data)





    #Ensure the correct user is logged in



    def test_incorrect_login(self):
        tester = app.test_client(self)
        with app.app_context():
            response = tester.post('/login', data=dict(username="wrong", password="wrong"), follow_redirects=True)
        self.assertIn(b'Invalid credentials, please try again.', response.data)

    
    def test_admin_loginnnc(self):
        tester = app.test_client(self)
        expectedPath = '/choose-test-topic'
        with app.app_context():
            #user_data = dict(username='admin', password='admin')
            response = tester.post('/login', data = dict(username='admin', password='admindd'), follow_redirects=True)
            assert response.status == '200 OK'
        self.assertEqual(urlparse(response.location).path, b'')

    

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
        tester = app.test_client(self)
        with tester.app_context():
            response = tester.post('/auth.login', data={
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

'''

if __name__ == '__main__':
    unittest.main(verbosity=2)
