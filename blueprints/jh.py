from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from jh.models import Yonghong,Users
from jh.forms import YonghongForm
from jh.extensions import db

jh_bp = Blueprint('jh',__name__)

@jh_bp.route('/yonghong_list',methods=['GET','POST'])
def yonghong_list():
    reports = Yonghong.query.order_by(Yonghong.id.desc())
    return render_template('jh/yonghonglist.html',reports=reports)

@jh_bp.route('/edit_yonghong/<int:yonghong_id>', methods=['POST', 'GET'])
def edit_yonghong(yonghong_id):
    report = Yonghong.query.get(yonghong_id)
    edit_form = YonghongForm()
    #username = Users.query.filter_by(id=current_user.id).first().username
    if edit_form.validate_on_submit():
        report.dev_status = edit_form.dev_status.data
        report.dev_name = edit_form.dev_name.data
        db.session.commit()
        flash('修改成功 ', 'success')
        return redirect(url_for('jh.yonghong_list'))
    edit_form.dev_status.data = report.dev_status
    edit_form.dev_name.data = report.dev_name
    return render_template('jh/edit_yonghong.html',target='_blank', form=edit_form, yonghong_id=yonghong_id,report=report)

