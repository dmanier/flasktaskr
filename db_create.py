__author__ = 'Damien'

from datetime import date

from project import db
from project.tasks.models import Task
from project.users.models import User
from project._config import adminname,adminpass,adminemail


db.create_all()

db.session.add(User(adminname, adminemail, adminpass,'admin'))

#db.session.add(Task("Finish Real Python", date(2015,5,20),date(2015,5,17), 10, 1,1))

db.session.commit()

