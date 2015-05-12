__author__ = 'Damien'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flastaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
CSRF_ENABLED = True
SECRET_KEY = b'\xa16@$\x80&\x1b\x159x3,5\xa8\xe9'

DATABASE_PATH = os.path.join(basedir,DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH