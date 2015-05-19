__author__ = 'Damien'

import os
import unittest

from project import app, db
from project._config import basedir
from project.users.models import User


TEST_DB = 'test.db'
name = 'Damien'
pw = 'password'
email = 'damien@damien.com'

class AllTests(unittest.TestCase):

    def login(self,user=name,password=pw):
        return self.app.post('/', data=dict(name=user, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def register(self,name=name, email=email, password=pw, confirm=pw):
        return self.app.post('register/', data=dict(name=name, email=email, password=password,confirm=confirm), follow_redirects=True)

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

    def test_user_already_logged_in_sent_to_tasks(self):
        self.register()
        self.login()
        response = self.app.get('/',follow_redirects=True)
        self.assertIn(b'Add new task:', response.data)

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)

    def test_users_can_login(self):
        self.register()
        response = self.login()
        self.assertIn(b'Welcome!',response.data)

    def test_invalid_form_data(self):
        self.register()
        response = self.login('alert("alert box!");','foo')
        self.assertIn(b'Invalid username or password', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_user_registration(self):
        self.assertIn(b'Thanks for registering. Please login.', self.register().data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register()
        self.assertIn(b'That username and/or email already exist.', self.register().data)

    def test_logged_in_user_can_log_out(self):
        self.register()
        self.login()
        self.assertIn(b'Goodbye!',self.logout().data)

    def test_not_logged_in_user_cannot_logout(self):
        self.assertNotIn(b'Goodbye!',self.logout().data)

    def test_logged_in_users_can_access_tasks_page(self):
        self.register()
        self.login()
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self. assertIn(b'Add new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_default_user_role(self):
        db.session.add(User(name,email,pw))
        db.session.commit()

        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(user.role,'user')

    def test_task_template_displays_logged_in_user_name(self):
        self.create_user()
        self.assertIn(name.encode('utf-8'),self.app.get('tasks/',follow_redirects=True).data)

if __name__ == '__main__':
    app.main()