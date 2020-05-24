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
            db.drop_all()




class UserLoginModel(TestBase):

    #Ensure Flask is setup correctly 
    def test_login_index(self):
        tester = app.test_client()
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    def test_register_index(self):
        tester = app.test_client()
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

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
        self.assertFalse(User.query.filter_by(username='lambo').first())
        self.assertNotIn(b'invalid details, try again.', response.data)
        self.assertIn(b'Invalid credentials, please try again.', response.data)
        

    #Ensure that the user can log in 
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = dict(
                username='akhil', 
                password='akhil'
                ),
            follow_redirects = True
        )
        self.assertTrue(User.query.filter_by(username='akhil').first())
        self.assertIn(b'Choose test topic', response.data)

    #Ensure that a new user can register
    #Ensure username can consists of letters (A-Z) and numbers (0-9)
    def test_register(self):
        tester = app.test_client(self)
        response = tester.post(
            '/register',
            data = dict(
                username='Johnny15', 
                password='Johnboi15'
                ),
            follow_redirects = True
        )
        #Test if the new user is in the datavase
        self.assertTrue(User.query.filter_by(username='Johnny15').first())
    

    #Ensure duplicate names are not registered in the database 
    def test_duplicates_name(self):
        tester = app.test_client(self)
        response = tester.post(
            '/register',
            data = dict(
                username='akhil', 
                password='akhil'
                ),
            follow_redirects = True
        )

        self.assertIn(b'Register', response.data)
        #checks if the user is already in the database
        #If the username already exists, new user cannot be registered, and therefore
        #and therefore, has to select a new username, in order to register
        self.assertIn(b'This username is taken, try again.', response.data)
        #self.assertFalse(User.query.filter_by(username='akhifll').all())

    '''
    def login(self, username, password):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username=username, password=password), follow_redirects=True)
        self.assertEqual(response.status_codec,200)

    '''

    #NEED TO CHECK USER LOGIN PASSWORD






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
        response = tester.get('/logout', follow_redirects=True)
        #print(response.data)
        #self.assertIn(b'Please log  in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are now logged out', response.data)
        #print(response.data)
        #self.assertIn(b'You are now logged out', response.data)

        #check if the user is logged out or still active


    #Ensure log in behaves correclty when fed with user data
    

#-------------------------------------------- Admin Page ---------------------------------------------------#

    #When the admin is logged in, the admin should be able to access the following pages 
    #   >/select-topics
    #   >/class-scores
    #   >/manage-students

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
        #self.assertTrue(current_user.id, 1)
        #print(responsedd.data)
        #checks choose-test-topic page works
        self.assertTrue(User.query.filter_by(username='admin').first())
        response_Select_Topics = tester.get('/select-topics', follow_redirects=True)
        self.assertEqual(response_Select_Topics.status_code, 200)
        self.assertIn(b'Welcome, Admin!', response_Select_Topics.data)
        self.assertIn(b'Toggle topics for students', response_Select_Topics.data)
        

        #checks my-score page works
        response_Class_Score = tester.get('/class-scores', follow_redirects=True)
        self.assertEqual(response_Class_Score.status_code, 200)
        self.assertIn(b'Welcome, Admin!', response_Class_Score.data)
        self.assertIn(b'Class scores', response_Class_Score.data)
        self.assertIn(b'Student', response_Class_Score.data)
        #self.assertIn(b'Class top score', response_My_Scores.data)

        #check manage-student page works
        response_Manage_Students = tester.get('/manage-students', follow_redirects=True)
        self.assertEqual(response_Manage_Students.status_code, 200)
        self.assertIn(b'Welcome, Admin!', response_Manage_Students.data)
        self.assertIn(b'Manage students', response_Manage_Students.data)
        self.assertIn(b'Students', response_Manage_Students.data)
        self.assertIn(b'Enable/Disable', response_Manage_Students.data)

    
    #When admin is logged in, the admin should be able to log out from its admistration
    #the page should redirect to the login page, once logout is clicked
    #with the output, You are now logged out'
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
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are now logged out', response.data)



  #-------------------------------------------- Student Page ---------------------------------------------------#


   #When the Student is logged in, the student should be able to access the following pages
   # >/choose-test-topic
   # >//my-scores

    def test_check_student_check_pages(self):
        
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='akhil', 
            password='akhil'), 
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        #checks choose-test-topic page works
        response_Test_Topics= tester.get('/choose-test-topic', follow_redirects=True)
        self.assertEqual(response_Test_Topics.status_code, 200)
        self.assertIn(b'Choose test topic', response_Test_Topics.data)
        self.assertIn(b'Welcome, akhil!', response_Test_Topics.data)

    
        #checks my-score page works
        response_My_Scores = tester.get('/my-scores', follow_redirects=True)
        self.assertEqual(response_My_Scores.status_code, 200)
        self.assertIn(b'My scores', response_My_Scores.data)
        self.assertIn(b'Topic', response_My_Scores.data)
        self.assertIn(b'Best score', response_My_Scores.data)
        self.assertIn(b'Class top score', response_My_Scores.data)

    
    #When student is logged in, student should be able to log out
    #Once, student logs out, the page will redirect to the log in page

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

        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Log in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are now logged out', response.data)
    
    #The user must authenicate itself before it can acccess the request
                                                          
    def test_give_auth(self):
        tester = app.test_client(self)
        url_login = '/login'

        url_scores = '/my-scores'
        respond_loginnn = tester.get(url_scores)
        print(respond_loginnn.status_code)
        print(respond_loginnn.data)
        self.assertEqual('If not click the link', respond_loginnn.data)



    '''
    #check if the correct user is logged in
    def test_redirect(self):
     
        tester = app.test_client(self)
        target_url = '/logout'
        redirect_url = '/login'
        responseClient = tester.get(target_url)

        print(responseClient .path)
        self.assertEqual(responseClient.status_code, 401)
    

    def test_login_and_registration(self):
        tester = app.test_client(self)
        login_url = '/login'
        logout_url = '/logout'
        responseClient = tester.get(login_url, follow_redirects=True)
        self.assertEqual(responseClient.url)
        print(responseClient.data)
    '''






#once you are logged, you shoudl not be able to go to the login or register page


#registration users with the same user name should not be allowed 

#--------------- Admin Login Page ---------------------------#


#check if i can go from login page to register page without any user logg requiremnet 


#print(response.data)


#Check each New User added to the data base is unquie


#Check the registration page can switch to login page 


#class TestUserModel(TestBase):


#Ensure the correct user is logged in



if __name__ == '__main__':
    unittest.main(verbosity=2)
