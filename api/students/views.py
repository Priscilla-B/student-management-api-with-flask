from flask_restx import Namespace, Resource

students_namespace = Namespace(
    'students',
    description='a namespace for student logic')


@students_namespace.route('/')
class StudentHello(Resource):

    def get(self):
        return {'message':'hello students!'}