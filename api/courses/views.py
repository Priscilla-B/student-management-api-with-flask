from flask_restx import Namespace, Resource

courses_namespace = Namespace(
    'courses',
    description='a namespace for course logic')