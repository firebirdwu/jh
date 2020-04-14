from jh.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class TaskType(db.Model):
    __tablename__ = "tasktype"
    id = db.Column(db.Integer, primary_key=True)
    tasklevel = db.Column(db.Integer)
    name = db.Column(db.String(30))


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30))
    taskType1 = db.Column(db.String(30))
    taskType2 = db.Column(db.String(30))
    taskName = db.Column(db.String(300))
    taskContent = db.Column(db.String(300))
    taskDate = db.Column(db.String(10))
    taskInputTime = db.Column(db.DateTime, default=datetime.utcnow)
    groupName = db.Column(db.Integer)

class TaskGroup(db.Model):
    __tablename__ = "taskgroup"
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(30))
