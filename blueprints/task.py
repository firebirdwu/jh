from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from jh.forms import TaskForm,SearchForm,TodoForm,CheckResultForm,ImportChecklist,BankcodeSearchForm  
from flask_login import login_required, current_user
from jh.models import Tasks,Todo,CheckResult,TaskGroup, TaskType, Users,BankCode
from jh.extensions import db,excel
from sqlalchemy import and_,or_


task_bp = Blueprint('task', __name__)


@task_bp.route('/tasklist',methods=['POST','GET'])
@login_required
def task_list():
    searchForm=SearchForm()
    if searchForm.validate_on_submit():
        username = Users.query.filter_by(id=current_user.id).first().username
        startdate = searchForm.dateStart.data
        enddate = searchForm.dateEnd.data
        #userexport=searchForm.userexport.data
        # if userexport:
        #     querySet=Tasks.query.filter(and_(Tasks.taskDate>=startdate, Tasks.taskDate <=enddate,Tasks.username==username)).all()
        #     columnNames=['username','groupName','taskType1','taskType2','taskName','taskContent','taskDate']
        #     return excel.make_response_from_query_sets(querySet,columnNames,"xls",file_name='tasks',sheet_name='tasks')
        
        # page = request.args.get('page', 1, type=int)
        # per_page = current_app.config['PER_PAGE']
        # paginate = Tasks.query.filter(and_(Tasks.taskDate>=startdate, Tasks.taskDate <=enddate,Tasks.username==username)).\
        #     order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
        # tasks= paginate.items
        tasks=Tasks.query.filter(and_(Tasks.taskDate>=startdate, Tasks.taskDate <=enddate,Tasks.username==username)).\
            order_by(Tasks.taskInputTime.desc())
        return render_template('task/tasklist.html', tasks=tasks,searchform=searchForm)
    else:
        username = Users.query.filter_by(id=current_user.id).first().username
        # page = request.args.get('page', 1, type=int)
        # per_page = current_app.config['PER_PAGE']
        # paginate = Tasks.query.filter_by(username=username).order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
        # tasks= paginate.items
        tasks=Tasks.query.filter_by(username=username).order_by(Tasks.taskInputTime.desc())
        return render_template('task/tasklist.html',tasks=tasks,searchform=searchForm)


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

@task_bp.route('/edit_checkresult/<int:check_id>', methods=['POST', 'GET'])
@login_required
def edit_checkresult(check_id):
    fckrst = CheckResultForm()
    result = CheckResult.query.filter_by(id=check_id).first()
    if fckrst.validate_on_submit():
        result.dealstatus = fckrst.dealstatus.data
        result.checkremark = fckrst.checkremark.data
        result.username = Users.query.filter_by(id=current_user.id).first().username
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('task.checkresult_list'))
    fckrst.checkcode.data =	result.checkcode
    fckrst.checkitemname.data = result.checkitemname
    fckrst.checklevel.data =	result.checklevel
    fckrst.checktable.data =	result.checktable
    fckrst.checktablename.data =result.checktablename 
    fckrst.checktableterm.data =result.checktableterm 
    fckrst.checksucflag.data = 	result.checksucflag
    fckrst.dmbegdate.data = 	result.dmbegdate
    fckrst.dmenddate.data = 	result.dmenddate
    fckrst.comcode.data = 	result.comcode
    fckrst.checksql.data = 	result.checksql
    fckrst.dealstatus.data = 	result.dealstatus
    fckrst.checkremark.data = 	result.checkremark
    fckrst.username.data =      result.username
    return render_template('task/edit_checkresult.html',edtform=fckrst,check_id=check_id,result=result)

@task_bp.route('/checkresult_list',methods=['POST','GET'])
@login_required
def checkresult_list():
        username = Users.query.filter_by(id=current_user.id).first().username
        #page = request.args.get('page', 1, type=int)
        #per_page = 20
        results = CheckResult.query.order_by(CheckResult.checklevel.desc())
        #results= paginate.items
        return render_template('task/checkresult_list.html',results=results)

@task_bp.route('/handson_view',methods=['GET'])
@login_required
def handson_table():
    return excel.make_response_from_tables(db.session,[CheckResult],'handsontable.html')

@task_bp.route('/export_table',methods=['GET'])
@login_required
def export_table():
    return excel.make_response_from_tables(db.session,[Tasks,Todo],"xls")


@task_bp.route('/import_checklist',methods=['POST','GET'])
@login_required
def import_checklist():
    importForm=ImportChecklist()
    
    if importForm.validate_on_submit():
        CheckResult.query.delete()
        def checkResult_init_func(row):
            cl=CheckResult()
            #cl.id = row['id']
            cl.checkcode = row['checkcode'] 
            cl.checkitemname = row['checkitemname'] 
            cl.checklevel = row['checklevel'] 
            cl.checktable = row['checktable'] 
            cl.checktablename = row['checktablename'] 
            cl.checktableterm = row['checktableterm'] 
            cl.checksucflag = row['checksucflag'] 
            cl.dmbegdate = row['dmbegdate'] 
            cl.dmenddate = row['dmenddate'] 
            cl.comcode = row['comcode']
            return cl
        request.save_book_to_database(
                field_name='filechecklist', 
                session=db.session,
                tables=[CheckResult],
                initializers=[checkResult_init_func])
        return redirect(url_for('.handson_table'),code=302)
    return render_template('task/import_checklist.html',form=importForm)

@task_bp.route('/bankcode_list',methods=['POST','GET'])
@login_required
def bankcode_list():
        bankSearchForm=BankcodeSearchForm()
        if bankSearchForm.validate_on_submit():
            searchText=bankSearchForm.searchText.data
            page = request.args.get('page', 1, type=int)
            per_page = 10
            paginate = BankCode.query.filter(or_(BankCode.bankcode.like('%'+searchText+'%'),BankCode.bankname.like('%'+searchText+'%'),BankCode.bankaddress.like('%'+searchText+'%'))).paginate(page, per_page=per_page)
            results= paginate.items
            return render_template('task/bankcode_list.html',searchform=bankSearchForm,results=results,pagination=paginate)
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 1000
            paginate = BankCode.query.paginate(page, per_page=per_page)
            results= paginate.items
            return render_template('task/bankcode_list.html',searchform=bankSearchForm, results=results,pagination=paginate)
