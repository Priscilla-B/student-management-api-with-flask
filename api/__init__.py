from flask import Flask
from flask_restx import Api

from .auth.views import auth_namespace
from .courses.views import courses_namespace
from .grading.views import grading_namespace
from .students.views import students_namespace
from .teachers.views import teachers_namespace
from .auth.models import User

from .config.config import config_dict
from .utils import db, migrate




def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(courses_namespace, path='/course')
    api.add_namespace(grading_namespace, path='')
    api.add_namespace(students_namespace, path='/student')
    api.add_namespace(teachers_namespace, path='/teacher')

    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User
        }

    return app