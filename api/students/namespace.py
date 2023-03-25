from flask_restx import Namespace

student_namespace = Namespace(
    'students',
    description='a namespace for student logic')
