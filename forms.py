from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField,ValidationError,HiddenField,\
    BooleanField,PasswordField
from wtforms.validators import DataRequired,Email,Length,Optional,URL

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('登录')

class RegistForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('密码',validators=[DataRequired(),Length(8,128)])
    repassword = PasswordField('确认密码',validators=[DataRequired(),Length(8,128)])
    submit = SubmitField('注册')