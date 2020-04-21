from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect


bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from jh.models import Users
    user=Users.query.get(int(user_id))
    return user

login_manager.login_view='auth.login'
login_manager.login_message_categoriy='warning'
login_manager.login_message='请先登录'