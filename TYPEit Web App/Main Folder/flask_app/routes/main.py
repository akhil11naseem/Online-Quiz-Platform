from flask import Blueprint, render_template, request, session, Response
from flask_login import current_user, login_required, logout_user
from flask_app.extensions import db
from flask_app.models import User, Topic, Results
from functools import wraps
import json

main = Blueprint('main', __name__)

def requires_admin_access():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(id=current_user.id).all()[0]
            if not user.admin:
                return ('<h1>You do not have admin access. Go back!</h1>', 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def requires_student_access():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(id=current_user.id).all()[0]
            if not user.student:
                return ('<h1>You are an admin. You are trying to access a student page. Go back!</h1>', 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@main.route('/change-password')
def changePassword():
    return '<h1>This page is in development. Go back!</h1>'

@main.route('/logout')
def logout():
    logged_out_message=''
    status_code=500
    if current_user.is_authenticated:
        logout_user()
        logged_out_message = "You are now logged out"
        status_code=200
    else:
        logged_out_message = "Please log in"
        status_code=401
    return (render_template('Dashboard/log in.html', message=logged_out_message), status_code)

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

@main.route('/update-manage-students', methods = ['POST','GET'])
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

@main.route('/update-available-topics', methods = ['POST','GET'])
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

@main.route('/question-page', methods = ['POST','GET'])
@login_required
@requires_student_access()
def questionPage():
    topic_name = request.args.get('topic_name')

    questions_arr = eval(Topic.query.filter_by(name=topic_name).first().questions)

    context = {
    'questions_arr' : questions_arr,
    'topic_name' : topic_name
    }

    return render_template('Game screens/question-page.html', **context)

@main.route('/results-page', methods = ['POST','GET'])
@login_required
@requires_student_access()
def resultsPage():
    context = {}
    if request.method == 'POST':
        resultsDict = request.get_json()
        context = {
            'score' : resultsDict['results2'][0],
            'numCorrectAnswers' : resultsDict['results2'][1],
            'longestStreak' : resultsDict['results2'][2],
            'accuracy' : resultsDict['results2'][3],
            'wordsAnswered' :  resultsDict['results2'][4]
        }

    return render_template('Game screens/results-page.html', name = current_user.username, **context)

@main.route('/update-results', methods = ['POST','GET'])
@login_required
@requires_student_access()
def updateResults():
    if request.method == 'POST':
        resultsDict = request.get_json()

        topic_id = Topic.query.filter_by(name=resultsDict['results'][1]).first().id

        student_id = current_user.id
        score = int(resultsDict['results'][0])

        myResult = Results.query.filter_by(result_of_user_id=student_id, result_for_topic_id=topic_id).first()

        if not myResult:
            insertResult = Results(score=score, result_of_user_id=student_id, result_for_topic_id=topic_id)
            db.session.add(insertResult)
            db.session.commit()
        else:
            myResult.score = score
            db.session.commit()

        return ("updated 'score' of user " + current_user.username + " to " + str(score))
