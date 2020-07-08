

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





class User(db.Model):
    '''User模型'''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'unknown'), default='unknown')
    birthday = db.Column(db.Date, default='1990-01-01')
    location = db.Column(db.String(10), nullable=False)
    bio = db.Column(db.String(256), default='')
    created = db.Column(db.DateTime)  # 用户注册时间
    avatar = db.Column(db.String(128), default='/static/img/default.jpg')


class Weibo(db.Model):
    '''微博表'''
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)

    @property
    def user(self):
        if not hasattr(self, '_user'):
            self._user = User.query.get(self.uid)
        return self._user

