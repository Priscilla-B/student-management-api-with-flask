from flask_restx import Namespace, Resource

grading_namespace = Namespace(
    'grading',
    description='a namespace for grading logic')


@grading_namespace.route('/')
class GradingHello(Resource):

    def get(self):
        return {'message':'here is the grading page!'}