from flask import Blueprint
from jh.DBUtils import DbUtil
from flask import render_template

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/',methods=['GET'])
def login():
    dbutil = DbUtil()
    users = dbutil.select('SELECT * FROM t_test')
    print(users)
    return render_template('auth/login.html',users=users)
