from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User

auth_namespace = Namespace(
    'auth',
    description='a namespace for authentication logic')


register_serializer = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description='first name of user'),
        'last_name': fields.String(required=True, description='last name of user'),
        'username': fields.String(required=True, description='public display name of user'),
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, 
                                  description='hash value of user password')
    }
)

@auth_namespace.route('/register')
class Register(Resource):

    @auth_namespace.expect(register_serializer)
    @auth_namespace.marshal_with(register_serializer)
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()

        new_user = User(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )

        new_user.save()

        # HTTPStatus.CREATED returns code 201 indicating 
        # that an object has been created
        return new_user, HTTPStatus.CREATED
        

    def get(self):
        return {'message':'hello auth!'}
    

@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        pass