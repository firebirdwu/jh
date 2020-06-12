from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from jh.forms import TaskForm, SearchForm, TodoForm, CheckResultForm, ImportChecklist, BankcodeSearchForm, SpeakerForm,SearchSpeakerForm
from flask_login import login_required, current_user
from jh.models import Tasks, Todo, CheckResult, TaskGroup, TaskType, Users, BankCode,Speakers
from jh.extensions import db, excel
from sqlalchemy import and_, or_
import json


task_bp = Blueprint('task', __name__)


@task_bp.route('/tasklist', methods=['POST', 'GET'])
@login_required
def task_list():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        username = Users.query.filter_by(id=current_user.id).first().username
        startdate = searchForm.dateStart.data
        enddate = searchForm.dateEnd.data
        # userexport=searchForm.userexport.data
        # if userexport:
        #     querySet=Tasks.query.filter(and_(Tasks.taskDate>=startdate, Tasks.taskDate <=enddate,Tasks.username==username)).all()
        #     columnNames=['username','groupName','taskType1','taskType2','taskName','taskContent','taskDate']
        #     return excel.make_response_from_query_sets(querySet,columnNames,"xls",file_name='tasks',sheet_name='tasks')

        # page = request.args.get('page', 1, type=int)
        # per_page = current_app.config['PER_PAGE']
        # paginate = Tasks.query.filter(and_(Tasks.taskDate>=startdate, Tasks.taskDate <=enddate,Tasks.username==username)).\
        #     order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
        # tasks= paginate.items
        tasks = Tasks.query.filter(and_(Tasks.taskDate >= startdate, Tasks.taskDate <= enddate, Tasks.username == username)).\
            order_by(Tasks.taskInputTime.desc())
        return render_template('task/tasklist.html', tasks=tasks, searchform=searchForm)
    else:
        username = Users.query.filter_by(id=current_user.id).first().username
        # page = request.args.get('page', 1, type=int)
        # per_page = current_app.config['PER_PAGE']
        # paginate = Tasks.query.filter_by(username=username).order_by(Tasks.taskInputTime.desc()).paginate(page, per_page=per_page)
        # tasks= paginate.items
        tasks = Tasks.query.filter_by(username=username).order_by(
            Tasks.taskInputTime.desc())
        return render_template('task/tasklist.html', tasks=tasks, searchform=searchForm)


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

@task_bp.route('/todolist', methods=['POST', 'GET'])
@login_required
def todo_list():
    username = Users.query.filter_by(id=current_user.id).first().username
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    paginate = Todo.query.filter(and_(Todo.username == username, Todo.tstatus == '完成')).order_by(
        Todo.id.desc()).paginate(page, per_page=per_page)
    todoes = paginate.items
    paginate2 = Todo.query.filter(and_(Todo.username == username, Todo.tstatus == '未完成')).order_by(
        Todo.id.desc()).paginate(page, per_page=per_page)
    undoes = paginate2.items
    return render_template('task/todolist_tabs.html', pagination=paginate, pagination2=paginate2, todoes=todoes, undoes=undoes)


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
        todo = Todo(tlevel=tlevel, tstatus=tstatus,
                    tcompletion=tcompletion, tcontent=tcontent, username=username)
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
        todo.username = Users.query.filter_by(
            id=current_user.id).first().username
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('task.todo_list'))
    todoform.tlevel.data = todo.tlevel
    todoform.tstatus.data = todo.tstatus
    todoform.tcompletion.data = todo.tcompletion
    todoform.tcontent.data = todo.tcontent
    return render_template('task/edit_todo.html', todoform=todoform, todo_id=todo_id)


@task_bp.route('/edit_checkresult/<int:check_id>', methods=['POST', 'GET'])
@login_required
def edit_checkresult(check_id):
    fckrst = CheckResultForm()
    result = CheckResult.query.filter_by(id=check_id).first()
    if fckrst.validate_on_submit():
        result.dealstatus = fckrst.dealstatus.data
        result.checkremark = fckrst.checkremark.data
        result.username = Users.query.filter_by(
            id=current_user.id).first().username
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('task.checkresult_list'))
    fckrst.checkcode.data = result.checkcode
    fckrst.checkitemname.data = result.checkitemname
    fckrst.checklevel.data = result.checklevel
    fckrst.checktable.data = result.checktable
    fckrst.checktablename.data = result.checktablename
    fckrst.checktableterm.data = result.checktableterm
    fckrst.checksucflag.data = result.checksucflag
    fckrst.dmbegdate.data = result.dmbegdate
    fckrst.dmenddate.data = result.dmenddate
    fckrst.comcode.data = result.comcode
    fckrst.checksql.data = result.checksql
    fckrst.dealstatus.data = result.dealstatus
    fckrst.checkremark.data = result.checkremark
    fckrst.username.data = result.username
    return render_template('task/edit_checkresult.html', edtform=fckrst, check_id=check_id, result=result)


@task_bp.route('/checkresult_list', methods=['POST', 'GET'])
@login_required
def checkresult_list():
    username = Users.query.filter_by(id=current_user.id).first().username
    #page = request.args.get('page', 1, type=int)
    #per_page = 20
    results = CheckResult.query.order_by(CheckResult.checklevel.desc())
    #results= paginate.items
    return render_template('task/checkresult_list.html', results=results)


@task_bp.route('/handson_view', methods=['GET'])
@login_required
def handson_table():
    return excel.make_response_from_tables(db.session, [CheckResult], 'handsontable.html')


@task_bp.route('/export_table', methods=['GET'])
@login_required
def export_table():
    return excel.make_response_from_tables(db.session, [Tasks, Todo], "xls")


@task_bp.route('/import_checklist', methods=['POST', 'GET'])
@login_required
def import_checklist():
    importForm = ImportChecklist()

    if importForm.validate_on_submit():
        CheckResult.query.delete()

        def checkResult_init_func(row):
            cl = CheckResult()
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
        return redirect(url_for('.handson_table'), code=302)
    return render_template('task/import_checklist.html', form=importForm)


@task_bp.route('/bankcode_list', methods=['POST', 'GET'])
@login_required
def bankcode_list():
    bankSearchForm = BankcodeSearchForm()
    if bankSearchForm.validate_on_submit():
        searchText = bankSearchForm.searchText.data
        page = request.args.get('page', 1, type=int)
        per_page = 10
        paginate = BankCode.query.filter(or_(BankCode.bankcode.like('%'+searchText+'%'), BankCode.bankname.like(
            '%'+searchText+'%'), BankCode.bankaddress.like('%'+searchText+'%'))).paginate(page, per_page=per_page)
        results = paginate.items
        return render_template('task/bankcode_list.html', searchform=bankSearchForm, results=results, pagination=paginate)
    else:
        page = request.args.get('page', 1, type=int)
        per_page = 1000
        paginate = BankCode.query.paginate(page, per_page=per_page)
        results = paginate.items
        return render_template('task/bankcode_list.html', searchform=bankSearchForm, results=results, pagination=paginate)


@task_bp.route('/speaker_list', methods=['POST', 'GET'])
@login_required
def speaker_list():
    searchForm = SearchSpeakerForm()
    if searchForm.validate_on_submit():
        dateStart = searchForm.dateStart.data
        dateEnd = searchForm.dateEnd.data
        searchValue = searchForm.searchvalue.data
        if dateStart == '' and dateEnd !='' or dateStart !='' and dateEnd =='':
            flash('开始时间或结束时间要同时有值','error')
            return ''
        if dateStart != '' and searchValue == '':
            results = Speakers.query.filter(and_(Speakers.deal_date>=dateStart,Speakers.deal_date < dateEnd))
        elif dateStart != '' and searchValue != '':
             results = Speakers.query.filter(and_(Speakers.deal_date>=dateStart,Speakers.deal_date < dateEnd)).\
                 filter(or_(Speakers.code.like('%'+searchValue+'%'),Speakers.speaker_name.like('%'+searchValue+'%')))
        else:
            results=Speakers.query.filter(or_(Speakers.code.like('%'+searchValue+'%'),Speakers.speaker_name.like('%'+searchValue+'%')))
        
        return render_template('task/speaker_list.html', speakers=results,searchform=searchForm)
    return render_template('task/speaker_list.html', speakers=None,searchform=searchForm)

@task_bp.route('/edit_seaker/<int:speaker_id>', methods=['POST', 'GET'])
@login_required
def edit_speaker(speaker_id):
    speaker = Speakers.query.get(speaker_id)
    edit_form = SpeakerForm()
    if edit_form.validate_on_submit():
        speaker.brand = edit_form.brand.data
        speaker.area = edit_form.area.data
        speaker.code = edit_form.code.data
        speaker.flag_1 = 'Y'
        speaker.username = edit_form.username.data
        speaker.speaker_name = edit_form.speaker_name.data
        speaker.speaker_level = edit_form.speaker_level.data
        speaker.city = edit_form.city.data
        speaker.zip_code = edit_form.zip_code.data
        speaker.hospital_name = edit_form.hospital_name.data
        speaker.section_office = edit_form.section_office.data
        speaker.speaker_name2 = edit_form.speaker_name.data
        speaker.flag_2 = 'Y'
        speaker.mobile_phone = edit_form.mobile_phone.data
        speaker.identify_number = edit_form.identify_number.data
        speaker.bank_information = edit_form.bank_information.data
        speaker.bank_city = edit_form.bank_city.data
        speaker.account_code = edit_form.account_code.data
        speaker.address = edit_form.address.data
        speaker.bank_code = edit_form.bank_code.data
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('task.speaker_list'))
    edit_form.brand.data=speaker.brand 
    edit_form.area.data=speaker.area 
    edit_form.code.data=speaker.code 
    edit_form.flag_1.data=speaker.flag_1 
    edit_form.username.data=speaker.username 
    edit_form.speaker_name.data=speaker.speaker_name 
    edit_form.speaker_level.data=speaker.speaker_level 
    edit_form.city.data=speaker.city 
    edit_form.zip_code.data=speaker.zip_code 
    edit_form.hospital_name.data=speaker.hospital_name 
    edit_form.section_office.data=speaker.section_office 
    edit_form.speaker_name2.data=speaker.speaker_name2 
    edit_form.flag_2.data=speaker.flag_2 
    edit_form.mobile_phone.data=speaker.mobile_phone 
    edit_form.identify_number.data=speaker.identify_number 
    edit_form.bank_information.data=speaker.bank_information 
    edit_form.bank_city.data=speaker.bank_city 
    edit_form.account_code.data=speaker.account_code 
    edit_form.address.data=speaker.address 
    edit_form.bank_code.data=speaker.bank_code
    return render_template('task/edit_speaker.html', form=edit_form, speaker_id=speaker_id)


@task_bp.route('/new_speaker', methods=['POST', 'GET'])
@login_required
def new_speaker():
    new_form = SpeakerForm()
    if new_form.validate_on_submit():
        brand = new_form.brand.data
        area = new_form.area.data
        code = new_form.code.data
        flag_1 = 'Y'
        username = new_form.username.data
        speaker_name = new_form.speaker_name.data
        speaker_level = new_form.speaker_level.data
        city = new_form.city.data
        zip_code = new_form.zip_code.data
        hospital_name = new_form.hospital_name.data
        section_office = new_form.section_office.data
        speaker_name2 = new_form.speaker_name.data
        flag_2 = 'Y'
        mobile_phone = new_form.mobile_phone.data
        identify_number = new_form.identify_number.data
        bank_information = new_form.bank_information.data
        bank_city = new_form.bank_city.data
        account_code = new_form.account_code.data
        address = new_form.address.data
        bank_code = new_form.bank_code.data
        speaker = Speakers(brand=brand,area=area,code=code,flag_1=flag_1,username=username,speaker_name=speaker_name,\
            speaker_level=speaker_level,city=city,zip_code=zip_code,hospital_name=hospital_name,section_office=section_office,\
                speaker_name2=speaker_name2,flag_2=flag_2,mobile_phone=mobile_phone,identify_number=identify_number,\
                    bank_information=bank_information,bank_city=bank_city,account_code=account_code,address=address,\
                        bank_code=bank_code)
        db.session.add(speaker)
        db.session.commit()
        flash('成功+1 ', 'success')
        return redirect(url_for('task.speaker_list'))
    return render_template('task/new_speaker.html', form=new_form)

@task_bp.route('/get_bankname/', methods=['POST', 'GET'])
def get_bankname():
    bankcode=request.args['bankcode']
    try:
        bankname=BankCode.query.filter_by(bankcode=bankcode).first().bankname
    except:
        bankname='未发现匹配银行信息'   
    data={'bankname':bankname}
    return json.dumps(data)

@task_bp.route('/get_speakerinfo/', methods=['POST', 'GET'])
def get_speakerinfo():
    code=request.args['code']
    try:
        speaker=Speakers.query.filter_by(code=code).first()
        data = speaker.to_json()
    except:
        data={'speaker_name':'None'}
    print(json.dumps(data))
    return json.dumps(data)
        