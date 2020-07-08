import datetime

from flask import Blueprint, request, redirect, url_for, render_template, session
from sqlalchemy.orm import exc

from App.models import User, db, Weibo

blue = Blueprint('blue', __name__)


@blue.route('/')
def hello_world():
    return 'Hello World!'


@blue.route('/register/',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        gender = request.form.get('gender')
        age = request.form.get('age')
        city = request.form.get('city')
        intro = request.form.get('intro')
        hobby = request.form.get('hobby')
        user = User(name=name, password=password, gender=gender, age=age, city=city, intro=intro, hobby=hobby)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('blue.login'))
    else:
        return render_template('register.html')


@blue.route('/login/', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':

        name = request.form.get('name')
        password = request.form.get('password')


        try:
            user = User.query.filter_by(name=name, password=password).one()
        except exc.NoResultFound:
            return render_template('login.html', err='用户名密码错误')


        session['uid'] = user.id
        session['name'] = user.name

        return redirect(url_for('blue.info'))
    else:
        return render_template('login.html')


@blue.route('/info/')
def info():
    if 'uid' in session:
        uid = session['uid']
        user = User.query.get(uid)
        return render_template('info.html', user=user)
    else:
        return redirect(url_for('blue.login'))


@blue.route('/sendWeibo/',methods=('GET', 'POST'))
def sendWeibo():
    if 'uid' not in session:
        return redirect(url_for('blue.login'))

    if request.method == 'POST':
        uid = session['uid']
        title = request.form.get('title')
        content = request.form.get('content')
        created = datetime.datetime.now()
        weibo = Weibo(uid=uid,title=title,content=content,created=created)

        db.session.add(weibo)
        db.session.commit()

        return redirect(url_for('blue.show_weibo'))
    else:
        return render_template('sendWeibo.html')


@blue.route('/show_weibo/')
def show_weibo():
    all_weibo = Weibo.query.all()
    return render_template('show_weibo.html',all_weibo=all_weibo)


@blue.route('/logout/')
def logout():
    session.pop('uid')
    session.pop('name')
    return redirect(url_for('blue.login'))