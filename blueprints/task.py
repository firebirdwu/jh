# -*- coding:utf-8 -*-
from flask import Blueprint, flash, render_template
from jh.forms import TaskForm
from flask_login import login_required,current_user
from jh.models import Tasks
from jh.extensions import db
from jh.models import TaskGroup,TaskType,Users


task_bp = Blueprint('task', __name__)



@task_bp.route('/new_task', methods=['POST', 'GET'])
@login_required
def new_task():
    new_form = TaskForm()
    if new_form.validate_on_submit():
        groupname=new_form.groupname.data
        tasktype1=new_form.taskType1.data
        tasktype2=new_form.taskType2.data
        taskname = new_form.taskName.data   
        taskcontent=new_form.taskContent.data
        taskdate = new_form.date.data
        username=Users.query.filter_by(id=current_user.id).first().username
        task= Tasks(username=username,taskDate=taskdate,groupName=groupname,taskType1=tasktype1,taskType2=tasktype2,taskName=taskname,taskContent=taskcontent)
        db.session.add(task)
        db.session.commit()
        flash('成功+1 ', 'success')
    return render_template('task/new_task.html', form=new_form)
