from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from jh.forms import LoginForm,RegistForm
from jh.models import Users
from jh.utils import redirect_back
from jh.extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        #return redirect(url_for('task.index'))
        return redirect(url_for('task.new_task'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        print(form.username.data)
        
        user = Users.query.filter_by(username=username).first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user,remember=remember)
                flash('欢迎回来.','info')
                #return redirect_back()
                return redirect(url_for('task.new_task'))
            flash("无效的用户名或密码.","warning")
        else:
            flash("无此账号!!","warning")
        
    return render_template('auth/login.html',form=form)

@auth_bp.route('/regist',methods=['POST','GET'])
def regist():
    reg_form=RegistForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        repassword= reg_form.repassword.data
        user=Users.query.filter_by(username=username).first()
        if user:

            flash("用户已存在!!","warning")
        else:
            if password!=repassword:
                flash("密码不一致!!","warning")
            else:
                try:
                    user=Users(username=username)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
                    form = LoginForm()
                    flash("恭喜%s注册成功" % username,"success")
                    return render_template('auth/login.html',form=form)
                except Exception as ex:
                    print(ex)
    return render_template('auth/register.html',reg_form=reg_form)



@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("欢迎下次再来.","info")
    return redirect_back(url_for('auth.login'))
