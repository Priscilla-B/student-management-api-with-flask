from flask_restx import Namespace, Resource

teachers_namespace = Namespace(
    'teachers',
    description='a namespace for teacher logic')


@teachers_namespace.route('/')
class TeacherHello(Resource):

    def get(self):
        return {'message':'hello teachers!'}