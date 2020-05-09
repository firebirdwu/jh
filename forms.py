from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField,\
    BooleanField, PasswordField,RadioField
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from wtforms.fields.html5 import DateField
from jh.models import TaskGroup,TaskType
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('登录')


class RegistForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    repassword = PasswordField(
        '确认密码', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('注册')


class TaskForm(FlaskForm):
    date=StringField("日期",validators=[DataRequired()],default=datetime.now().strftime('%Y-%m-%d'))
    groupname = SelectField('归属组', coerce=str, default=1)
    taskType1 = SelectField('任务类型1', coerce=str, default=1)
    taskType2 = SelectField('任务类型2', coerce=str, default=1)
    taskName = TextAreaField('任务名称', validators=[DataRequired()])
    taskContent = TextAreaField('任务详情', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(TaskForm,self).__init__(*args,**kwargs)
        self.groupname.choices = [(group.groupname,group.groupname) for group in TaskGroup.query.order_by(TaskGroup.id).all()]
        self.taskType1.choices = [(task.name,task.name) for task in TaskType.query.filter_by(tasklevel=1).order_by(TaskType.id).all()]
        self.taskType2.choices = [(task.name,task.name) for task in TaskType.query.filter_by(tasklevel=2).order_by(TaskType.id).all()]
    
class SearchForm(FlaskForm):
    dateStart=StringField("开始日期:",validators=[DataRequired()])
    dateEnd=StringField("结束日期:",validators=[DataRequired()])
    submit = SubmitField('查询')
    
class TodoForm(FlaskForm):
    tlevel = RadioField('级别:',coerce=str,choices=[('一般','一般'),('重要','重要'),('紧急','紧急')],default=1)
    tstatus = RadioField('状态:',coerce=str,choices=[('未完成','未完成'),('完成','完成')],default=1)
    tcompletion = SelectField('完成度:', coerce=str, default='50%',choices=[('0%','0%'),('50%','50%'),('80%','80%'),('100%','100%')])
    tcontent = TextAreaField('任务名称', validators=[DataRequired()])
    submit = SubmitField('确认')

class CheckResultForm(FlaskForm):
    checkcode =StringField("校验代码:")
    checkitemname = StringField("规则描述")
    checklevel = StringField("规则级别")
    checktable = StringField("表名:")
    checktablename = StringField("表名中文")
    checktableterm = StringField("规则分组:")
    checksucflag = StringField("校验结果:")
    dmbegdate = StringField("起始时间:")
    dmenddate =StringField("结束时间:")
    comcode = StringField("机构代码:")
    checksql = StringField("校验SQL:")
    dealstatus = SelectField('处理进度:', coerce=str, default='未完成',choices=[('未完成','未完成'),('已完成','已完成')])
    checkremark = TextAreaField("处理备注:")
    username = StringField("处理人:")
    submit = SubmitField('确认')