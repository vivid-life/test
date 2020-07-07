from flask import Blueprint, request, redirect, url_for, render_template, session
from sqlalchemy.orm import exc

from App.models import User, db

blue = Blueprint('blue',__name__)

@blue.route('/')
def hello_world():
    return 'Hello World!'


@blue.route('/register/')
def register():
    if request.method =='POST':
        name = request.form.get('name')
        password = request.form.get('password')
        gender = request.form.get('gender')
        age = request.form.get('age')
        city = request.form.get('city')
        intro = request.form.get('intro')
        hobby = request.form.get('hobby')
        user = User(name=name,password=password,gender=gender,age=age,city=city,intro=intro
                    ,hobby=hobby)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('blue.login'))
    else:
        return render_template('register.html')


@blue.route('/login/', methods=('GET', 'POST'))
def login():
    '''登录'''
    if request.method == 'POST':
        # 取出参数
        username = request.form.get('username')
        password = request.form.get('password')

        # 取出用户数据, 并检查 (无法取到时需要提示用户密码错误)
        try:
            user = User.query.filter_by(username=username, password=password).one()
        except exc.NoResultFound:
            return render_template('login.html', err='用户名密码错误')

        # 将登录状态记录到 session
        session['uid'] = user.id
        session['username'] = user.username

        return redirect(url_for('blue.info'))  # 返回用户信息页
    else:
        return render_template('login.html')