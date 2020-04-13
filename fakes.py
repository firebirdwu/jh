from jh.models import Users,TaskType,Tasks
from jh.extensions import db
from faker import Faker

faker = Faker()

def fake_users():
    user=Users(username='firebird')
    user.set_password('123456')
    db.session.add(user)
    db.session.commit()

def faker_taskType():
    taskType1=TaskType(
        level=1,
        name=faker.name()
    )
    taskType2=TaskType(
        level=2,
        name=faker.name()
    )
    db.session.add([taskType1,taskType2])
    db.session.commit()

