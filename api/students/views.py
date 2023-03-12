from flask_restx import Namespace, Resource

students_namespace = Namespace(
    'students',
    description='a namespace for student logic')