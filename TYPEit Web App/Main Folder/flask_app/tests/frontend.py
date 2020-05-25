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
from selenium.webdriver.common.by import By


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app=create_app(config_file='test_settings.py')
app.testing = True
app.test_client()

# --------------------------------- Global Variables ---------------------------------------- #


class TestBase(unittest.TestCase):
    driver = None
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))
        if not self.driver:
            self.skipTest
        else:
            with app.app_context():
                db.session.commit()
                db.drop_all()
                db.create_all()
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

        button_field = self.driver.find_element_by_id('log-in-register-btn').click()
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('akhil')
        password_field = self.driver.find_element_by_id('password-input').send_keys('akhil')
        button_field = self.driver.find_element_by_id('register-btn').click()
        username_taken_message = self.driver.find_element_by_class_name('alert').text
        self.assertEqual(username_taken_message, 'This username is taken, try again.')

    
    def test_register(self):
        button_field = self.driver.find_element_by_id('log-in-register-btn').click()
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('lukeee')
        password_field = self.driver.find_element_by_id('password-input').send_keys('Morty1234')
        button_field = self.driver.find_element_by_id('register-btn').click()
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username-input').send_keys('lukeee')
        password_field = self.driver.find_element_by_id('password-input').send_keys('Morty1234')
        button_field = self.driver.find_element_by_id('log-in-btn').click()
        time.sleep(3)
    

class TestLogin(TestBase):
    
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
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_partial_link_text("Class").click()
        time.sleep(5)
        self.driver.find_element_by_partial_link_text("Manage").click()
        time.sleep(2)
        #self.driver.find_element_by_partial_link_text("Change").click()
        #time.sleep(2)
        self.driver.find_element_by_partial_link_text("Log").click()
        time.sleep(2)
        username_taken_message = self.driver.find_element_by_class_name('alert').text
        self.assertEqual(username_taken_message, 'You are now logged out')
    
    
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
        greetings = self.driver.find_element_by_id('Welcome').get_attribute('innerHTML')
        self.assertIn(greetings, 'Welcome, akhil!')
        #self.driver.find_element_by_partial_link_text("My").click()
        #time.sleep(5)
        self.driver.find_element_by_partial_link_text("Log").click()
        time.sleep(2)
        username_taken_message = self.driver.find_element_by_class_name('alert').text
        self.assertEqual(username_taken_message, 'You are now logged out')
    
    

#admin disables a topic, student cannot click on that quix

#disable user 

'''

    def test_disable_student(self):
         
        time.sleep(2)
        user = self.driver.find_element_by_id('username-input').send_keys('admin')
        password = self.driver.find_element_by_id('password-input').send_keys('admin')
        time.sleep(1)
        button = self.driver.find_element_by_id('log-in-btn').click()
        time.sleep(0.5)
        self.driver.find_element_by_partial_link_text("Manage").click()
        time.sleep(2)
        user = User.query.filter_by(username='akhil').all()
        self.driver.find_element_by_class_name('student-switch-label').click()
        self.driver.find_element_by_partial_link_text("Log").click()
        username_taken_message = self.driver.find_element_by_class_name('alert').text
        time.sleep(3)
        self.assertEqual(username_taken_message, 'You are now logged out')
        time.sleep(6)
        #if user.enabled is False:
        #    self.driver.find_element_by_class_name('student-switch-label').click()
        user = self.driver.find_element_by_id('username-input').send_keys('akhil')
        password = self.driver.find_element_by_id('password-input').send_keys('akhil')
        button = self.driver.find_element_by_id('log-in-btn').click()
        disabed = self.
        if user.enabled is False: 
            username_disabled_message = self.driver.find_element_by_id('alert-message').text
            self.assertEqual(username_disabled_message, 'User disabled, contact Admin.')
            time.sleep(2)
        else: 
            self.driver.find_element_by_partial_link_text("My").click()
            time.sleep(2)



    '''

class TestQuiz(TestBase):

    def test_play_quiz(self):
        time.sleep(2)
        user = self.driver.find_element_by_id('username-input').send_keys('akhil')
        password = self.driver.find_element_by_id('password-input').send_keys('akhil')
        time.sleep(1)
        button = self.driver.find_element_by_id('log-in-btn').click()
        time.sleep(0.5)
        button = self.driver.find_element_by_id('English').click()
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('i')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('m')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('p')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('r')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('o')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('m')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('p')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('t')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('u')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('h')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('a')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('i')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('k')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('u')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('d')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('e')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('x')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('t')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('e')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('r')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('i')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('t')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('y')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('p')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('h')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('o')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('b')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('i')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('a')
        time.sleep(0.5)
        button = self.driver.find_element_by_id('skip-btn').click()
        time.sleep(0.5)
        button = self.driver.find_element_by_id('skip-btn').click()
        time.sleep(1)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('d')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('e')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('r')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('v')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('i')
        time.sleep(1)
        button = self.driver.find_element_by_id('skip-btn').click()
        time.sleep(1)
        button = self.driver.find_element_by_id('skip-btn').click()
        time.sleep(1)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('t')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('o')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('r')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('q')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('u')
        time.sleep(0.5)
        self.driver.find_element_by_id('hint-and-answer-input').send_keys('e')
        time.sleep(1)
        button = self.driver.find_element_by_id('skip-btn').click()
        time.sleep(3)
        button = self.driver.find_element_by_id('play-again-btn').click()
        time.sleep(2)
        self.driver.find_element_by_partial_link_text("My").click()
        time.sleep(2)





if __name__=='__main__':
  unittest.main(verbosity=2)
        
        





