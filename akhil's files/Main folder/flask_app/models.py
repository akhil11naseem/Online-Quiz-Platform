from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# topics_results_m2m_table = db.Table(
# 'topics_results_m2m_table',
# db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
# db.Column('results_id', db.Integer, db.ForeignKey('results.id'))
# ) INITIALLY THOUGHT RESULTS/TOPIC IS M-M BUT IS ACTUALLY 1-M, SO THIS BLOCK IS NOT NEEDED

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    student = db.Column(db.Boolean)
    enabled = db.Column(db.Boolean)

    results = db.relationship('Results', backref='user_results')

    def __init__(self, username, password, admin, student, enabled):
        self.username = username
        self.password = password 
        self.admin = admin
        self.student = student
        self.enabled = enabled


    def is_admin(self):
        return self.admin

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

    @property 
    def username_id(self):
        return '{}'.format(self.username)

    @property 
    def is_student(self):
        return self.student

    @property 
    def is_enabled(self):
        return self.enabled


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    questions = db.Column(db.Text(30))
    enabled = db.Column(db.Boolean)

    results = db.relationship('Results', backref='topic_results')

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    result_of_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result_for_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
