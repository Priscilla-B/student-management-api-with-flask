from flask_restx import Namespace, Resource

auth_namespace = Namespace(
    'auth',
    description='a namespace for authentication logic')


@auth_namespace.route('/register')
class Register(Resource):

    def post(self):
        pass

    def get(self):
        return {'message':'hello auth!'}
    

@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        pass