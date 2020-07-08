import os
from hashlib import sha256
from functools import wraps

from flask import session
from flask import redirect


def make_password(password):
    '''产生一个安全的密码'''
    hash_value = sha256(password.encode('utf8')).hexdigest()
    salt = os.urandom(32).hex()
    return salt + hash_value


def check_password(password, safe_password):
    '''检查密码'''
    hash_value = sha256(password.encode('utf8')).hexdigest()
    return hash_value == safe_password[64:]


def login_required(view_function):
    '''装饰器：检查用户是否登录'''
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if 'uid' in session:
            return view_function(*args, **kwargs)
        else:
            return redirect('/user/login')
    return wrapper


def save_avatar(uid, avatar):
    '''保存用户上传的头像'''
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'Avatar-%s' % uid
    filepath = os.path.join(project_dir, 'static', 'upload', filename)  # 文件在硬盘上的绝对路径
    avatar.save(filepath)

    file_url = os.path.join('/static', 'upload', filename)  # 文件的 URL
    return file_url
