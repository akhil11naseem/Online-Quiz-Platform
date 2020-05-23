from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    admin = db.Column(db.Boolean, default=False)
    student = db.Column(db.Boolean, default=True)
    enabled = db.Column(db.Boolean, default=True)

    results = db.relationship('Results', backref='user_results')


    def is_admin(self):
        return self.admin

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)




class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    questions = db.Column(db.Text(30))
    enabled = db.Column(db.Boolean, default=True)

    results = db.relationship('Results', backref='topic_results')


    def __init__(self, name, questions, enabled):
        self.name = name
        self.questions=questions
        self.enabled = enabled

    @property
    def name_id(self):
        return '{}'.format(self.name)



    @property
    def is_enabled(self):
        return self.enabled

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    result_of_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result_for_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
