__author__ = 'Damien'

import datetime
from functools import wraps

from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
from .forms import AddTaskForm
from .models import Task
from project import db

tasks_blueprint = Blueprint('tasks', __name__)



def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

def same_user(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    if session['user_id'] == task.first().user_id or session['role']=='admin':
        return task
    else:
        return None

def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

@tasks_blueprint.route('/tasks/')
@login_required
def tasks():
    return render_template('tasks.html',form=AddTaskForm(request.form),open_tasks=open_tasks(),closed_tasks=closed_tasks(),username=session['name'])

@tasks_blueprint.route('/add/', methods=['GET','POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(form.name.data, form.due_date.data,datetime.datetime.utcnow(), form.priority.data,'1',session['user_id'])
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was successfully posted. Thanks.")
            return redirect(url_for('tasks.tasks'))
    return render_template('tasks.html', form = form, error=error, open_tasks=open_tasks(), closed_tasks=closed_tasks())

@tasks_blueprint.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    task = same_user(task_id)
    if task:
        task.update({'status':'0'})
        db.session.commit()
        flash('The task was marked complete.')
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks.tasks'))

@tasks_blueprint.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    task = same_user(task_id)
    if task:
        task.delete()
        db.session.commit()
        flash('The task was deleted.')
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks.tasks'))