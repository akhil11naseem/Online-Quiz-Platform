from flask import Blueprint, render_template

from flask_app.extensions import db
from flask_app.models import User, Topic, Results

main = Blueprint('main', __name__)

@main.route('/change-password')
def changePassword():
    return render_template('Dashboard/change password.html')

@main.route('/class-scores')
def classScores():
    return render_template('Dashboard/Admin dashboard/class scores.html')

@main.route('/manage-students')
def manageStudents():

    students = User.query.filter_by(student=True).all()
    print(students)

    context = {
        'students' : students
    }

    return render_template('Dashboard/Admin dashboard/manage students.html', **context)

@main.route('/select-topics')
def selectTopics():

    topics = Topic.query.all()

    context = {
        'topics' : topics
    }

    return render_template('Dashboard/Admin dashboard/select topics.html', **context)

@main.route('/choose-test-topic')
def chooseTestTopic():
    return render_template('Dashboard/Student dashboard/student - choose test topic.html')

@main.route('/my-scores')
def myScores():
    return render_template('Dashboard/Student dashboard/student - my scores.html')

@main.route('/question-page')
def questionPage():
    return render_template('Game screens/question-page.html')

@main.route('/results-page')
def resultsPage():
    return render_template('Game screens/results-page.html')