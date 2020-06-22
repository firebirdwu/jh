from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField,\
    BooleanField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError
from wtforms.fields.html5 import DateField
from jh.models import TaskGroup, TaskType
from datetime import datetime
from jh.utils import check_identify


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


class SearchForm(FlaskForm):
    dateStart = StringField("开始日期:", validators=[DataRequired()])
    dateEnd = StringField("结束日期:", validators=[DataRequired()])
    userexport = BooleanField('导出')
    submit = SubmitField('确定')


class TaskForm(FlaskForm):
    date = StringField("日期", validators=[DataRequired(
    )], default=datetime.now().strftime('%Y-%m-%d'))
    groupname = SelectField('归属组', coerce=str, default=1)
    taskType1 = SelectField('任务类型1', coerce=str, default=1)
    taskType2 = SelectField('任务类型2', coerce=str, default=1)
    taskName = TextAreaField('任务名称', validators=[DataRequired()])
    taskContent = TextAreaField('任务详情', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.groupname.choices = [(group.groupname, group.groupname)
                                  for group in TaskGroup.query.order_by(TaskGroup.id).all()]
        self.taskType1.choices = [(task.name, task.name) for task in TaskType.query.filter_by(
            tasklevel=1).order_by(TaskType.id).all()]
        self.taskType2.choices = [(task.name, task.name) for task in TaskType.query.filter_by(
            tasklevel=2).order_by(TaskType.id).all()]


class TodoForm(FlaskForm):
    tlevel = RadioField('级别:', coerce=str, choices=[
                        ('一般', '一般'), ('重要', '重要'), ('紧急', '紧急')], default=1)
    tstatus = RadioField('状态:', coerce=str, choices=[
                         ('未完成', '未完成'), ('完成', '完成')], default=1)
    tcompletion = SelectField('完成度:', coerce=str, default='50%', choices=[
                              ('0%', '0%'), ('50%', '50%'), ('80%', '80%'), ('100%', '100%')])
    tcontent = TextAreaField('任务名称', validators=[DataRequired()])
    submit = SubmitField('确认')


class CheckResultForm(FlaskForm):
    checkcode = StringField("校验代码:")
    checkitemname = StringField("规则描述")
    checklevel = StringField("规则级别")
    checktable = StringField("表名:")
    checktablename = StringField("表名中文")
    checktableterm = StringField("规则分组:")
    checksucflag = StringField("校验结果:")
    dmbegdate = StringField("起始时间:")
    dmenddate = StringField("结束时间:")
    comcode = StringField("机构代码:")
    checksql = StringField("校验SQL:")
    dealstatus = SelectField('处理进度:', coerce=str, default='未完成', choices=[
                             ('未完成', '未完成'), ('已完成', '已完成')])
    checkremark = TextAreaField("处理备注:")
    username = StringField("处理人:")
    submit = SubmitField('确认')


class ImportChecklist(FlaskForm):

    filechecklist = StringField("file", validators=[DataRequired()])
    submit = SubmitField('确认')


class ImportForm(FlaskForm):

    filespeakerlist = StringField("file", validators=[DataRequired()])
    submit = SubmitField('确认')


class BankcodeSearchForm(FlaskForm):
    searchText = StringField("查询条件:", validators=[DataRequired()])
    submit = SubmitField('确定')


class SpeakerForm(FlaskForm):
    brand = StringField("品牌:")
    area = StringField("大区信息:")
    code = StringField("code:")
    flag_1 = StringField("flag_1:")
    username = StringField("处理人:")
    speaker_name = StringField("讲者名称:")
    speaker_level = StringField("讲者级别:")
    city = StringField("城市:")
    zip_code = StringField("邮编:")
    hospital_name = StringField("医院名称:")
    section_office = StringField("科室:")
    speaker_name2 = StringField("讲者2:")
    flag_2 = StringField("flag_2:")
    mobile_phone = StringField("讲者手机号:")
    identify_number = StringField("身份证号:")
    bank_information = StringField("开户网点信息:")
    bank_city = StringField("银行所在城市:")
    account_code = StringField("开户账号:")
    address = StringField("地址:")
    bank_code = StringField("bankcode:")
    deal_date = StringField('处理日期:')
    remark = TextAreaField('备注:')
    id_type = RadioField('证件类型:', coerce=str, choices=[
                         ('身份证', '身份证'), ('护照', '护照'), ('其他', '其他')], default=1)
    submit = SubmitField('确定')

    def validate_identify_number(form, field):
        field_data = field.data
        print('##############################checking##################')
        print('######################'+form.id_type.data)
        if form.id_type.data == '身份证':
            if len(field_data) != 18:
                raise ValidationError('当身份类型为身份证时，长度必须为18')
            elif not (check_identify(field_data)[0]):
                raise ValidationError('身份证不符合身份证编码规则')
        elif form.id_type.data == '护照':
            if len(field_data) != 7:
                raise ValidationError('护照长度不符，应为7位')


class YonghongForm(FlaskForm):
    dev_name = StringField('开发人:')
    dev_status = SelectField('开发进度:', coerce=str, default='未完成', choices=[
                             ('未完成', '未完成'), ('已完成', '已完成')])
    submit = SubmitField('确定')


class SearchSpeakerForm(FlaskForm):
    dateStart = StringField("开始日期:")
    dateEnd = StringField("结束日期:")
    searchvalue = StringField("检索信息")
    submit = SubmitField('确定')
