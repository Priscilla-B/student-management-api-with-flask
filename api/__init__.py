from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from .auth.views import auth_namespace
from .courses.views import course_namespace
from .grading.views import grading_namespace
from .students.views import student_namespace
from .auth.models import User

from .config.config import config_chosen
from .utils import db, migrate




def create_app(config=config_chosen):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(grading_namespace, path='/grade')
    api.add_namespace(student_namespace, path='/students')

    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User
        }

    return app