#import modules
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user

from flask_app.extensions import db
from flask_app.models import User, Topic, Results
#Using flask blueprint for resource use with routes
auth = Blueprint('auth', __name__)
#default route for website returns user to login
@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

#route for registration
@auth.route('/register', methods=['GET', 'POST'])
def register():
    error_message = ''
#check if user is already logged in and displays error message
    if current_user.is_authenticated:
        return '<h1 id="h1_error">Already logged in, go back.</h1>'
        #get user input for username and unhashed password for new entry into database
    if request.method=='POST':
        username = request.form['username']
        unhashed_password = request.form['password']
#check if username has been registered before and display error message

        if User.query.filter_by(username=username).all():
            error_message = 'This username is taken, try again.'

        else:
#sets user privileges to student and then committ to db
#get all results from db and add top score

            user = User(
                username=username,
                unhashed_password=unhashed_password,
                admin=False,
                student=True,
                enabled=True
            )
            db.session.add(user)
            db.session.commit()

            for topic in Topic.query.all():
                result = Results(
                    result_of_user_id = User.query.filter_by(username=username).first().id,
                    result_for_topic_id = topic.id
                )
                db.session.add(result)
                db.session.commit()


#redirect back to login page after registration process
            return redirect(url_for('auth.login'))
#return values to html page
    return render_template('Dashboard/register.html', message=error_message)

@auth.route('/login', methods=['GET', 'POST'])
def login():
#check if user is already authenticated and trying to access this site
    error_message = ''
    if current_user.is_authenticated:
        return '<h1 id="h1_error">Already logged in, go back.</h1>'
#Check if correct password or username
    if request.method == 'POST':
        username = request.form['username']
        unhashed_password = request.form['password']

        user = User.query.filter_by(username=username).first()
#If user exists and is disabled by admin, show message to user
        if not user or not check_password_hash(user.password, unhashed_password):
            error_message = 'Invalid credentials, please try again.'

        elif not user.enabled:
            error_message = 'User disabled, contact Admin.'
#redirect to respective pages
        else:
            login_user(user)
            if user.admin:
                return redirect(url_for('main.selectTopics'))
            if user.student:
                return redirect(url_for('main.chooseTestTopic'))


    return render_template('Dashboard/log in.html', message=error_message)
