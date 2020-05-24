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


class SystemTest(unittest.TestCase):
    driver = None
    def setUp(self):
        with app.app_context():
            db.session.commit()
            db.drop_all()
            db.create_all()
            self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))
            self.driver.implicitly_wait(30)
            #self.base_url = 'http://localhost:5000/'
            admin = User(username="admin", password=generate_password_hash("admin"), admin=True, student=False, enabled=True)
            student1 = User(username='akhil',password=generate_password_hash('akhil'), admin=False, student=True, enabled=True)
            db.session.add(admin)
            db.session.add(student1)
            db.session.commit()
            #db.drop_all()

            self.driver.maximize_window()
           

    def tearDown(self):
        with app.app_context():
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()

    def test_login(self):
        self.driver.get('http://localhost:5000/login')

        user_field = self.driver.find_element_by_id('username-input').send_keys('Tom')
        password_field = self.driver.find_element_by_id('password-input').send_keys('passwrd')
        button_field = self.driver.find_element_by_id('log-in-btn').click()
        invalid = self.driver.find_element_by_id('alert-message').text
        self.assertEqual(invalid, 'Invalid credentials, please try again.')
     
        
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