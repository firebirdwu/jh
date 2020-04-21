from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from jh.forms import TaskForm
from flask_login import login_required, current_user
from jh.models import Tasks
from jh.extensions import db
from jh.models import TaskGroup, TaskType, Users


task_bp = Blueprint('task', __name__)


@task_bp.route('/tasklist')
@login_required
def task_list():
    username = Users.query.filter_by(id=current_user.id).first().username
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    paginate = Tasks.query.filter_by(username=username).order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
    tasks= paginate.items
    return render_template('task/tasklist.html', pagination=paginate, tasks=tasks)


@task_bp.route('/new_task', methods=['POST', 'GET'])
@login_required
def new_task():
    new_form = TaskForm()
    if new_form.validate_on_submit():
        groupname = new_form.groupname.data
        tasktype1 = new_form.taskType1.data
        tasktype2 = new_form.taskType2.data
        taskname = new_form.taskName.data
        taskcontent = new_form.taskContent.data
        taskdate = new_form.date.data
        username = Users.query.filter_by(id=current_user.id).first().username
        task = Tasks(username=username, taskDate=taskdate, groupName=groupname,
                     taskType1=tasktype1, taskType2=tasktype2, taskName=taskname, taskContent=taskcontent)
        db.session.add(task)
        db.session.commit()
        flash('成功+1 ', 'success')
        return redirect(url_for('task.task_list'))
    return render_template('task/new_task.html', form=new_form)


@task_bp.route('/edit_task/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit_task(task_id):
    task = Tasks.query.get(task_id)
    edit_form = TaskForm()
    if edit_form.validate_on_submit():
        task.groupName = edit_form.groupname.data
        task.taskType1 = edit_form.taskType1.data
        task.taskType2 = edit_form.taskType2.data
        task.taskName = edit_form.taskName.data
        task.taskContent = edit_form.taskContent.data
        task.taskDate = edit_form.date.data
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('task.task_list'))
    edit_form.groupname.data = task.groupName
    edit_form.taskType1.data = task.taskType1
    edit_form.taskType2.data = task.taskType2
    edit_form.taskName.data = task.taskName
    edit_form.taskContent.data = task.taskContent
    edit_form.date.data = task.taskDate
    #edit_form.username.data = task.username

    return render_template('task/edit_task.html', form=edit_form, task_id=task_id)
