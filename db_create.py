__author__ = 'Damien'

from views import db
from models import Task
from datetime import date

db.create_all()

db.session.add(Task("Finish this tutorial", date(2015,5,15), 10, 1))

db.session.add(Task("Finish Real Python", date(2015,5,15), 10, 1))

db.session.commit()

