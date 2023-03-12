from flask import Flask
from flask_restx import Api

from .auth.views import auth_namespace
from .courses.views import courses_namespace
from .grading.views import grading_namespace
from .students.views import students_namespace
from .teachers.views import teachers_namespace

from .config.config import config_dict


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    api = Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(courses_namespace, path='/course')
    api.add_namespace(grading_namespace, path='')
    api.add_namespace(students_namespace, path='/student')
    api.add_namespace(teachers_namespace, path='/teacher')

    return app