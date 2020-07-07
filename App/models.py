import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Gender(enum.Enum):
    '''性别的枚举类'''
    male = 1
    female = 2
    unknow = 3

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    password = db.Column(db.String(32))
    gender = db.Column(db.Enum(Gender), default='unknown')
    age = db.Column(db.Integer)
    city = db.Column(db.String(20))
    intro = db.Column(db.String(128))
    hobby = db.Column(db.String(64))


class Weibo(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    topic = db.Column(db.String(32), nullable=False, index=True)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime, nullable=False)