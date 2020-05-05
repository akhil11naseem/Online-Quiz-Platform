from flask import render_template 
from app import app
from app.forms import LoginForm, RegistrationForm

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = "Login Form", form = form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title = "Register", form = form)
