from selenium import webdriver
import unittest, os, time
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
from flask_testing import LiveServerTestCase


basedir = os.path.abspath(os.path.dirname(__file__))

#driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))
#driver.get('http://localhost:5000/')
#time.sleep(1)
#driver.find_element_by_name('username').send_keys('Tom')
#driver.find_element_by_name('password').send_keys('pw')

app = Flask(__name__)
app=create_app(config_file='test_settings.py')
app.testing = True
app.test_client()

# --------------------------------- Global Variables ---------------------------------------- #

test_admin_user = 'admin'
test_admin_password='admin'

test_incorrect_user='luke'
test_incorrecct_password='skywalker123'

test_student_user = 'akhil'
test_student_password = 'akhil'

class TestBase(unittest.TestCase):
    driver = None
    def setUp(self):
        with app.app_context():
            db.session.commit()
            db.drop_all()
            db.create_all()
            self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))
            self.driver.implicitly_wait(30)
            self.base_url = 'http://localhost:5000/'
            admin = User(username="admin", password=generate_password_hash("admin"), admin=True, student=False, enabled=True)
            student1 = User(username='akhil',password=generate_password_hash('akhil'), admin=False, student=True, enabled=True)
            db.session.add(admin)
            db.session.add(student1)
            db.session.commit()
            #db.drop_all()
            self.driver.get('http://localhost:5000/login')
            self.driver.maximize_window()
           

    def tearDown(self):
        #self.driver.quit()
        with app.app_context():
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()


#New user should be able to successfully create an account
#Once, the user is registered, the browser should redirect to the login page
    
class TestRegisteration(TestBase):

    def test_invalid_register(self):

        #user = User.query.filter_by(username='akhil').first()
        button_field = self.driver.find_element_by_id('log-in-register-btn').click()
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('akhil')
        password_field = self.driver.find_element_by_id('password-input').send_keys('akhil')
        button_field = self.driver.find_element_by_id('register-btn').click()
        username_taken_message = self.driver.find_element_by_class_name('alert').text
        self.assertEqual(user.username, user_field)
        self.assertEqual(username_taken_message, 'This username is taken, try again.')


    def test_register(self):
        button_field = self.driver.find_element_by_id('log-in-register-btn').click()
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('Ridkkk')
        password_field = self.driver.find_element_by_id('password-input').send_keys('Morty1234')
        button_field = self.driver.find_element_by_id('register-btn').click()
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('Ridkkk')
        password_field = self.driver.find_element_by_id('password-input').send_keys('Morty1234')
        button_field = self.driver.find_element_by_id('log-in-btn').click()
        time.sleep(3)
    

class TestLogin(TestBase):

    def test_login_by_student(self):
        time.sleep(2)
        user = self.driver.find_element_by_id('username-input').send_keys('akhil')
        password = self.driver.find_element_by_id('password-input').send_keys('akhil')
        time.sleep(1)
        button = self.driver.find_element_by_id('log-in-btn').click()
        time.sleep(0.5)
        self.driver.get(self.base_url+'/choose-test-topic')
        #admin access
        #self.driver.get(self.base_url+'/select-topics')
        time.sleep(2)
        greetings = self.driver.find_element_by_id('Welcome').text
        self.assertIn(greetings, 'Welcome, akhil!')

    def test_login_by_admin(self):
        time.sleep(2)
        user = self.driver.find_element_by_id('username-input').send_keys('admin')
        password = self.driver.find_element_by_id('password-input').send_keys('admin')
        time.sleep(1)
        button = self.driver.find_element_by_id('log-in-btn').click()
        time.sleep(0.5)
        self.driver.get(self.base_url+'/select-topics')
        #admin access
        #self.driver.get(self.base_url+'/select-topics')
        time.sleep(2)
        greetings = self.driver.find_element_by_id('Welcome').text
        self.assertIn(greetings, 'Welcome, Admin!')

    '''
class TestLogin(TestBase):


    def test_login(self):
        time.sleep(1)
        #admin login 
        user_field = self.driver.find_element_by_id('username-input').send_keys('admin')
        password_field = self.driver.find_element_by_id('password-input').send_keys('admin')
        button_field = self.driver.find_element_by_id('log-in-btn').click()

        #Application should redirect to the Select Topics Page
        self.driver.get(self.base_url+'/select-topics')
        welcome_message = self.driver.find_element_by_id('Welcome').get_attribute('innerHTML')
        self.assertIn(welcome_message, 'Welcome, Admin!')










    #incorrect login details, user is not in database
    def test_incorrect_login(self):
     
        time.sleep(1)
        
        user_field = self.driver.find_element_by_id('username-input').send_keys('abfnd')
        #self.driver.find_element_by_name('username-input').clear()
        password_field = self.driver.find_element_by_id('password-input').send_keys('asbhdjn')
        #self.driver.find_element_by_name('password-input').clear()
        button_field = self.driver.find_element_by_id('log-in-btn').click()
  
     
    

    def test_correct_login(self):
        
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('akhil')
        password_field = self.driver.find_element_by_id('password-input').send_keys('akhil')
        button_field = self.driver.find_element_by_id('log-in-btn').click()






    '''





if __name__=='__main__':
  unittest.main(verbosity=2)
        
        
       # tester = app.test_client()
       # response = tester.get('/', content_type='html/text')
        #self.assertEqual(response.status_code, 302)
        #admin = User.query.get(1)
        #self.assertEquals(admin.username, 'Test')
        #userr = User.query.filter_by(username='admin')
        #driver = self.driver 
       # self.driver.get('http://localhost:5000/')

       # user = driver.find_element_by_name('username').send_keys('admin')
       # passwd = driver.find_element_by_name('password').send_keys('admin')
       # assertEqual(userr, user)




'''
class Login(object):

    def __init__()


'''
















#launch the browser fireforx, naviagte to url and look for element (textbox by name q) then type in software testing in there


#ccreate driver object - instalise the webbroswer with firefox
#basedir = os.path.abspath(os.path.dirname(__file__))

#navigate to the following URL
#driver.get('http://localhost:5000/')


#driver.find_element_by_name('username').send_keys('software testing')