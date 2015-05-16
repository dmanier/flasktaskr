__author__ = 'Damien'
import datetime
from views import db

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, due_date, posted_date,priority, status, user_id):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def __repr__(self):
        return '<name {0}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='poster')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.name)