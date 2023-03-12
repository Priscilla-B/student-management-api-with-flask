from flask_restx import Namespace, Resource

grading_namespace = Namespace(
    'grading',
    description='a namespace for grading logic')