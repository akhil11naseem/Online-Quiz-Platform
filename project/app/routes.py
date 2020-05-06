from flask import render_template, flash, url_for, redirect
from app import app
from app.forms import LoginForm, RegistrationForm

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash('You have been successfully logged in', 'success')
            return(redirect(url_for('manage_students')))
        else: 
            flash('Login Failed. Please check password and username', 'error')
    return render_template('login.html', title = "Login Form", form = form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title = "Register", form = form)

@app.route('/students')
def manage_students():
    return render_template('manage-students.html', title="Students-Admin")

@app.route('/scores')
def scores():
    return render_template('class-scores.html', title="Students-Admin")
