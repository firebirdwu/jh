from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from jh.forms import TaskForm,SearchForm,TodoForm
from flask_login import login_required, current_user
from jh.models import Tasks,Todo
from jh.extensions import db
from jh.models import TaskGroup, TaskType, Users
from sqlalchemy import and_


task_bp = Blueprint('task', __name__)


@task_bp.route('/tasklist',methods=['POST','GET'])
@login_required
def task_list():
    searchForm=SearchForm()
    if searchForm.validate_on_submit():
        startdate = searchForm.dateStart.data
        enddate = searchForm.dateEnd.data
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['PER_PAGE']
        paginate = Tasks.query.filter(and_(Tasks.taskDate>=startdate, Tasks.taskDate <=enddate)).\
            order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
        tasks= paginate.items
        return render_template('task/tasklist.html', pagination=paginate, tasks=tasks,searchform=searchForm)
    else:
        username = Users.query.filter_by(id=current_user.id).first().username
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['PER_PAGE']
        paginate = Tasks.query.filter_by(username=username).order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
        tasks= paginate.items
        return render_template('task/tasklist.html', pagination=paginate, tasks=tasks,searchform=searchForm)


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



@task_bp.route('/todolist',methods=['POST','GET'])
@login_required
def todo_list():
        username = Users.query.filter_by(id=current_user.id).first().username
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['PER_PAGE']
        paginate = Todo.query.filter(and_(Todo.username==username,Todo.tstatus=='完成')).order_by(Todo.id.desc()).paginate(page, per_page=per_page)
        todoes= paginate.items
        paginate2 = Todo.query.filter(and_(Todo.username==username,Todo.tstatus=='未完成')).order_by(Todo.id.desc()).paginate(page, per_page=per_page)
        undoes= paginate2.items
        return render_template('task/todolist_tabs.html', pagination=paginate, pagination2=paginate2, todoes=todoes,undoes=undoes)



@task_bp.route('/new_todo', methods=['POST', 'GET'])
@login_required
def new_todo():
    todoform = TodoForm()
    if todoform.validate_on_submit():
        tlevel = todoform.tlevel.data
        tstatus = todoform.tstatus.data
        tcompletion = todoform.tcompletion.data
        tcontent = todoform.tcontent.data
        username = Users.query.filter_by(id=current_user.id).first().username
        todo = Todo(tlevel=tlevel,tstatus=tstatus,tcompletion=tcompletion,tcontent=tcontent,username=username)
        db.session.add(todo)
        db.session.commit()
        flash('成功+1 ', 'success')
        return redirect(url_for('task.todo_list'))
    return render_template('task/new_todo.html', todoform=todoform)

@task_bp.route('/edit_todo/<int:todo_id>', methods=['POST', 'GET'])
@login_required
def edit_todo(todo_id):
    todoform = TodoForm()
    todo = Todo.query.filter_by(id=todo_id).first()
    if todoform.validate_on_submit():
        todo.tlevel = todoform.tlevel.data
        todo.tstatus = todoform.tstatus.data
        todo.tcompletion = todoform.tcompletion.data
        todo.tcontent = todoform.tcontent.data
        todo.username = Users.query.filter_by(id=current_user.id).first().username
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('task.todo_list'))
    todoform.tlevel.data=todo.tlevel
    todoform.tstatus.data=todo.tstatus
    todoform.tcompletion.data=todo.tcompletion 
    todoform.tcontent.data=todo.tcontent 
    return render_template('task/edit_todo.html', todoform=todoform,todo_id=todo_id)
