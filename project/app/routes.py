from flask import render_template, flash, url_for, redirect
from app import app
from app.forms import LoginForm




@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash('You have been successfully logged in', 'success')
            return(redirect(url_for('students')))
        else: 
            flash('Login Failed. Please check password and username', 'error')
    return render_template('login.html', title = "Login Form", form = form)


@app.route('/scores')
def scores():
    return render_template('class-scores.html')

@app.route('/students')
def students():
    return render_template('manage-students.html', title='manage students')

@app.route('/topics')
def topics():
    return render_template('toggle-topics.html', title='manage students')

@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        my_data = Data(name)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return redirect(url_for('scores'))