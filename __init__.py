from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from jh.settings import config
from jh.blueprints.admin import admin_bp
from jh.blueprints.auth import auth_bp
from jh.blueprints.task import task_bp
from jh.extensions import mail, db, bootstrap, moment, ckeditor,csrf,login_manager,excel
from flask import render_template
from jh.DBUtils import DbUtil
from jh.models import Users
from flask_login import current_user
import click
import os


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('jh')
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_template_context(app)
    return app


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    excel.init_excel(app)


def register_blueprints(app):
    app.register_blueprint(task_bp,url_prefix='/task')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/about')
    def about():
        return render_template('about/about.html')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400


def register_commands(app):
    """
    @app.cli.command()
    @click.option('--test',is_flag=True,help='xxxxx')
    def insert_information():
        dbutils = DbUtil()
        from  datetime import datetime
        import click
        try:
            dbutils.update('insert into t_test values(:name,:time,:dm_com_code)',{'name':'firebird','time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'dm_com_code':'33020000'})
            click.echo('插入成功')
        except Exception as e:
            click.echo(e)
            click.echo('插入失败')
    """
    @app.cli.command()
    @click.option('--drop',is_flag=True,help='create after drop')
    def initdb(drop):
        """ initialize the database """
        if drop:
            click.confirm('this operation will drop database ,are you sure continue?',abort=True)
            db.drop_all()
            click.echo('drop tables')
        db.create_all()
        click.echo('initialized database.')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            user=Users.query.filter_by(id=current_user.id).first()
        else:
            user=None
        return dict(user=user)