from jh.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json


class Users(db.Model, UserMixin):
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
    username = db.Column(db.String(30))
    groupName = db.Column(db.String(30))
    taskType1 = db.Column(db.String(30))
    taskType2 = db.Column(db.String(30))
    taskName = db.Column(db.String(300))
    taskContent = db.Column(db.String(300))
    taskDate = db.Column(db.String(10))
    taskInputTime = db.Column(db.DateTime, default=datetime.utcnow)


class TaskGroup(db.Model):
    __tablename__ = "taskgroup"
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(30))


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    tcontent = db.Column(db.String(300))
    tlevel = db.Column(db.String(10))
    tstatus = db.Column(db.String(10), default='未完成')
    username = db.Column(db.String(30))
    tcompletion = db.Column(db.String(5))


class CheckResult(db.Model):
    __tablename__ = "CheckResult"
    id = db.Column(db.Integer, primary_key=True)
    checkcode = db.Column(db.String(50))
    checkitemname = db.Column(db.String(255))
    checklevel = db.Column(db.String(50))
    checktable = db.Column(db.String(50))
    checktablename = db.Column(db.String(50))
    checktableterm = db.Column(db.String(50))
    checksucflag = db.Column(db.String(50))
    dmbegdate = db.Column(db.String(50))
    dmenddate = db.Column(db.String(50))
    comcode = db.Column(db.String(20))
    checksql = db.Column(db.String(500))
    dealstatus = db.Column(db.String(10))
    checkremark = db.Column(db.String(500))
    username = db.Column(db.String(500))


class BankCode(db.Model):
    __tablename__ = "BankCode"
    id = db.Column(db.Integer, primary_key=True)
    codetype = db.Column(db.String(50))
    bankcode = db.Column(db.String(50))
    bankname = db.Column(db.String(200))
    bankaddress = db.Column(db.String(1000))


class Speakers(db.Model):
    __tablename__ = "Speakers"
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    area = db.Column(db.String(50))
    code = db.Column(db.String(50))
    flag_1 = db.Column(db.String(50))
    username = db.Column(db.String(50))
    speaker_name = db.Column(db.String(50))
    speaker_level = db.Column(db.String(50))
    city = db.Column(db.String(50))
    zip_code = db.Column(db.String(50))
    hospital_name = db.Column(db.String(50))
    section_office = db.Column(db.String(50))
    speaker_name2 = db.Column(db.String(50))
    flag_2 = db.Column(db.String(50))
    mobile_phone = db.Column(db.String(50))
    identify_number = db.Column(db.String(50))
    bank_information = db.Column(db.String(50))
    bank_city = db.Column(db.String(50))
    account_code = db.Column(db.String(50))
    address = db.Column(db.String(500))
    bank_code = db.Column(db.String(50))
    deal_date = db.Column(db.String(20))
    remark = db.Column(db.String(1000))
    id_type = db.Column(db.String(10))

    def to_json(self):
        data = {
            'id': self.id,
            'brand': self.brand,
            'area': self.area,
            'code': self.code,
            'flag_1': self.flag_1,
            'username': self.username,
            'speaker_name': self.speaker_name,
            'speaker_level': self.speaker_level,
            'city': self.city,
            'zip_code': self.zip_code,
            'hospital_name': self.hospital_name,
            'section_office': self.section_office,
            'speaker_name2': self.speaker_name2,
            'flag_2': self.flag_2,
            'mobile_phone': self.mobile_phone,
            'identify_number': self.identify_number,
            'bank_information': self.bank_information,
            'bank_city': self.bank_city,
            'account_code': self.account_code,
            'address': self.address,
            'bank_code': self.bank_code,
            'deal_date': self.deal_date,
            'remark': self.remark,
            'id_type': self.id_type
        }
        return data
    

class Yonghong(db.Model):
    __tablename__ = 'yonghong'
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(50))
    dev_status = db.Column(db.String(20))
    dev_name = db.Column(db.String(50))
