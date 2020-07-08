import datetime

from flask import Blueprint, request, redirect, url_for, render_template, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc

from App.models import User, db, Weibo
from App.utils import make_password, check_password, save_avatar, login_required

blue = Blueprint('blue', __name__)


@blue.route('/')
def hello_world():
    return 'Hello World!'


@blue.route('/register/',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        location = request.form.get('location','').strip()
        bio = request.form.get('bio')

        if username == '' or password == '':
            return render_template('register.html',error='昵称和密码不能为空')
        safe_password = make_password(password)

        user = User(username=username, password=password, gender=gender,
                    birthday=birthday, location=location, bio=bio, created=datetime.datetime.now())

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', err="昵称已存在，请换一个")
        else:
            return redirect(url_for('blue.login'))
    else:
        return render_template('register.html')


@blue.route('/login/', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':

        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()


        try:
            user = User.query.filter_by(username=username, password=password).one()
        except exc.NoResultFound:
            return render_template('login.html', err='用户名密码错误')

        if check_password(password, user.password):

            session['uid'] = user.id
            session['username'] = user.username

            return redirect(url_for('blue.info'))
        else:
            return render_template('login.html', err='用户名或密码错误')

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


@blue.route('/logout/')
def logout():
    session.pop('uid')
    session.pop('username')
    return redirect(url_for('blue.login'))


@blue.route('/update/')
@login_required
def update():
    uid = session['uid']
    user = User.query.get(uid)

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        location = request.form.get('location', '').strip()
        bio = request.form.get('bio', '').strip()
        avatar = request.files.get('avatar')

        if username == '':
            return render_template('update.html', err="昵称不允许为空！")

        user.username = username
        user.gender = gender
        user.birthday = birthday
        user.location = location
        user.bio = bio

        # 检查并保存用户头像
        if avatar:
            avatar_url = save_avatar(uid, avatar)
            user.avatar = avatar_url

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('update.html', err="昵称已存在，请换一个", user=user)
        else:
            session['username'] = username
            return redirect('/user/info')
    else:

        return render_template('update.html', user=user)

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


