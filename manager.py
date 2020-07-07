
from flask_script import Manager

from App import create_app
from App.views import blue

app = create_app()

manager = Manager(app=app)

app.register_blueprint(blueprint=blue)



if __name__ == '__main__':
    manager.run()
