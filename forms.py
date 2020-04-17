from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField,\
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from wtforms.fields.html5 import DateField
from jh.models import TaskGroup,TaskType

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
    date=DateField("日期",validators=[DataRequired()])
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