from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required, logout_user
from flask_app.extensions import db
from flask_app.models import User, Topic, Results
from functools import wraps

main = Blueprint('main', __name__)

def requires_admin_access():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(id=current_user.id).all()[0]
            if not user.admin:
                return '<h1>You do not have admin access!</h1>'
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def requires_student_access():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(id=current_user.id).all()[0]
            if not user.student:
                return '<h1>You are an admin. You are trying to access a student page!</h1>'
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@main.route('/change-password')
def changePassword():
    return '<h1>This page is not ready yet</h1>'

@main.route('/logout')
@login_required
def logout():
    logout_user()
    logged_out_message = "You are now logged out"
    return render_template('Dashboard/log in.html', message=logged_out_message)

@main.route('/class-scores')
@login_required
@requires_admin_access()
def classScores():
    results = Results.query.filter_by().all()
    students = User.query.filter_by(student=True).all()
    topics = Topic.query.all()

    context = {
        'results' : results,
        'students' : students,
        'topics' : topics
    }

    return render_template('Dashboard/Admin dashboard/class scores.html',  **context)

@main.route('/manage-students')
@login_required
@requires_admin_access()
def manageStudents():
    students = User.query.filter_by(student=True).all()

    context = {
        'students' : students
    }

    return render_template('Dashboard/Admin dashboard/manage students.html', **context)

@main.route('/update-manage-students')
@login_required
@requires_admin_access()
def updateManageStudents():
    id = int(request.args.get('id'))
    checked = request.args.get('checked')

    if checked == "true":
        update_val = 1;
    else:
        update_val = 0;

    student = User.query.get(id)
    student.enabled = update_val
    db.session.commit()

    return ("updated 'enabled' column of student " + student.username + " to " + checked)



@main.route('/select-topics')
@login_required
@requires_admin_access()
def selectTopics():

    topics = Topic.query.all()

    context = {
        'topics' : topics
    }

    return render_template('Dashboard/Admin dashboard/select topics.html', **context)

@main.route('/update-available-topics')
@login_required
@requires_admin_access()
def updateAvailableTopics():
    id = int(request.args.get('id'))
    checked = request.args.get('checked')

    if checked == "true":
        update_val = 1;
    else:
        update_val = 0;

    topic = Topic.query.get(id)
    topic.enabled = update_val
    db.session.commit()

    return ("updated 'enabled' column of topic " + topic.name + " to " + checked)

@main.route('/choose-test-topic')
@login_required
@requires_student_access()
def chooseTestTopic():
    topics = Topic.query.all()

    context = {
    'topics' : topics
    }
    return render_template('Dashboard/Student dashboard/student - choose test topic.html', name = current_user.username, **context)

    return render_template('Dashboard/Student dashboard/student - choose test topic.html')

@main.route('/my-scores')
@login_required
@requires_student_access()
def myScores():
    myResults = Results.query.filter_by(result_of_user_id=current_user.id).all()

    topResults_rowproxy = db.engine.execute("SELECT result_for_topic_id, score FROM( SELECT *, ROW_NUMBER()OVER(PARTITION BY result_for_topic_id ORDER BY score DESC) rn FROM Results)X WHERE rn = 1")
    topResults = [{column: value for column, value in rowproxy.items()} for rowproxy in topResults_rowproxy]


    topics = Topic.query.all()

    context = {
        'topResults' : topResults,
        'myResults' : myResults,
        'topics' : topics
    }

    return render_template('Dashboard/Student dashboard/student - my scores.html', name = current_user.username,  **context)

@main.route('/question-page')
@login_required
@requires_student_access()
def questionPage():
    return render_template('Game screens/question-page.html')

@main.route('/results-page')
@login_required
@requires_student_access()
def resultsPage():
    return render_template('Game screens/results-page.html')
