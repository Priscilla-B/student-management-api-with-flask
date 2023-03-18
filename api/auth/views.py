from http import HTTPStatus
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, get_jwt_identity)
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


login_serializer = auth_namespace.model(
    'Login', {
    'email':fields.String(required=True, description='user email address'),
    'password': fields.String(required=True, 
                                  description='user input of password')
    }
)


get_user_serializer = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description='first name of user'),
        'last_name': fields.String(required=True, description='last name of user'),
        'username': fields.String(required=True, description='public display name of user'),
        'email': fields.String(required=True, description='user email address'),
    }
)


group_serializer = auth_namespace.model(
    'Group', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description='name of user group'),
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
        
    
    

@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_serializer)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.OK

@auth_namespace.route('/users')
class GetUsers(Resource):
    @jwt_required()
    @auth_namespace.marshal_with(get_user_serializer)
    def get(self):

        users = User.query.all()

        return users, HTTPStatus.OK
    

@auth_namespace.route('/users/user/<int:pk>')
class GetUpdateDeleteUser(Resource):
    @jwt_required()
    @auth_namespace.marshal_with(get_user_serializer)
    def get(self,pk):

        user = User.query.filter_by(id=pk).first_or_404()

        return user, HTTPStatus.OK




@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)


        return {'access_token': access_token}, HTTPStatus.OK