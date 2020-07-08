from flask import Flask
from flask_migrate import Migrate
from flask_session import Session

from App.models import db


def create_app():
    app = Flask(__name__)

    # session
    app.config['SECRET_KEY'] = '110'
    app.config['SESSION_TYPE'] = 'redis'
    Session(app=app)

    # sqlalchemy
    # dialect+driver://root:password@host:port/database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ccc!950607@49.235.21.234:3306/lianxi3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app=app)

    # migrate
    migrate = Migrate()
    migrate.init_app(app=app, db=db)
    return app
