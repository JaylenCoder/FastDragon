import peewee
from peewee import (
    ForeignKeyField,
    TextField,
    BooleanField,
    IntegerField,
    CharField,
    FloatField,
    DoubleField,
    DateField,
    DateTimeField,
    AutoField,
    Proxy,
    Model, SQL,
)

# database = MySQLDatabase('fast_dragon',
#                          **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1',
#                             'port': 3306, 'user': 'root', 'password': '123456'})
from peewee_async import Manager
from playhouse.reflection import UnknownField

from app.main.database import db, PeeweeGetterDict


class BaseModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = db.atomic_async
        self.object = Manager(db)

    class Meta:
        database = db


class Aerich(BaseModel):
    app = CharField()
    content = UnknownField()  # json
    version = CharField()

    class Meta:
        table_name = 'aerich'


class User(BaseModel):
    avatar = CharField(null=True)
    created_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP(6)")], null=True)
    creator_id = CharField()
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    dept_id = IntegerField(null=True)
    email = CharField(null=True)
    login_ip = CharField()
    login_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP(6)")], null=True)
    modified_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP(6)")], null=True)
    password = CharField()
    phone = CharField(null=True)
    real_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    remark = CharField(null=True)
    status = CharField(constraints=[SQL("DEFAULT '1'")])
    super_admin = CharField(constraints=[SQL("DEFAULT '0'")])
    tag = CharField(null=True)
    uid = CharField(unique=True)
    user_name = CharField(unique=True)

    class Meta:
        table_name = 'user'
