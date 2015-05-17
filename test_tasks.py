__author__ = 'Damien'

import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'
name = 'Damien'
pw = 'password'
email = 'damien@damien.com'

class AllTests(unittest.TestCase):

    def create_user(self,name=name,email=email,password=pw,role='user'):
        new_user = User(name=name, email=email, password=password,role=role)
        db.session.add(new_user)
        db.session.commit()
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)


    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
         db.drop_all()

    def create_task(self,**kwargs):
        return self.app.post('add/', data=dict(name=kwargs.get('name','Go to the bank'),
                                               due_date=kwargs.get('due_date','05/20/2015'),
                                               priority=kwargs.get('priority','1'),
                                               posted_date=kwargs.get('posted_date','05/16/2015'),
                                               status=kwargs.get('status','1')), follow_redirects=True)

    def test_users_can_add_tasks(self):
        self.create_user()
        self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'New entry was successfully posted. Thanks', self.create_task().data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user()
        self.app.get('tasks/',follow_redirects=True)
        response = self.create_task(due_date='')
        self.assertIn(b'This field is required',response.data)

    def test_users_can_complete_tasks(self):
        self.create_user()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task was marked complete.', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.app.get('tasks/',follow_redirects=True)
        self.create_task()
        self.app.get('logout/', follow_redirects=True)
        self.create_user(name='Fletch',email='fletch@fletch.com')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'The task was marked complete.', response.data)
        self.assertIn(b'You can only update tasks that belong to you.',response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.app.get('tasks/',follow_redirects=True)
        self.create_task()
        self.app.get('logout/', follow_redirects=True)
        self.create_user(name='Fletch',email='fletch@fletch.com')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertNotIn(b'The task was deleted', response.data)
        self.assertIn(b'You can only update tasks that belong to you.',response.data)

    def test_admin_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.app.get('tasks/',follow_redirects=True)
        self.create_task()
        self.app.get('logout/', follow_redirects=True)
        self.create_user(name='Fletch',email='fletch@fletch.com',role='admin')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task was marked complete.', response.data)
        self.assertNotIn(b'You can only update tasks that belong to you.',response.data)

    def test_admin_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.app.get('tasks/',follow_redirects=True)
        self.create_task()
        self.app.get('logout/', follow_redirects=True)
        self.create_user(name='Fletch',email='fletch@fletch.com',role='admin')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted', response.data)
        self.assertNotIn(b'You can only update tasks that belong to you.',response.data)

if __name__ == '__main__':
    app.main()