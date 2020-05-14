from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

topics_results_m2m_table = db.Table(
'topics_results_m2m_table',
db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
db.Column('results_id', db.Integer, db.ForeignKey('results.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    student = db.Column(db.Boolean)

    results = db.relationship('Results', backref='user_results')

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topicName = db.Column(db.String(30))
    questions = db.Column(db.Text(30))

    results = db.relationship(
    'Results',
    secondary = topics_results_m2m_table,
    backref = 'topicResults'
    )

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    result_of_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result_for_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
