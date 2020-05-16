from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user

from flask_app.extensions import db
from flask_app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('Dashboard/log in.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username = request.form['username']
        unhashed_password = request.form['password']

        user = User(
            username=username,
            unhashed_password=unhashed_password,
            admin=False,
            student=True
        )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('Dashboard/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        unhashed_password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, unhashed_password):
            error_message = 'Invalid credentials, please try again.'

        elif not user.enabled:
            error_message = 'User disabled, contact Admin.'

        else:
            login_user(user)
            if user.admin:
                return redirect(url_for('main.selectTopics'))
            if user.student:
                return redirect(url_for('main.chooseTestTopic'))


    return render_template('Dashboard/log in.html', error=error_message)
