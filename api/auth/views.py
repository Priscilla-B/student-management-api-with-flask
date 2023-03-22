from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, get_jwt_identity)
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .mixins import UserCreationMixin

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
                                  description='hash value of user password'),
        'role':fields.String(required=True, 
                            decription='role for user, whether staff or admin.',
                            # enum=[role for role in Role.query.all() if role.name is not "student" ]
                                  )                    
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
        'role': fields.String(required=True, 
                                  description='hash value of user password') 
    }
)


role_serializer = auth_namespace.model(
    'Role', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description='name of user group'),
    }
)


@auth_namespace.route('/register')
class Register(Resource, UserCreationMixin):

    @auth_namespace.expect(register_serializer)
    @auth_namespace.marshal_with(register_serializer)
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()

        new_user = self.create_user(data)
       

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
    

@auth_namespace.route('/users/<int:pk>')
class GetUpdateDeleteUser(Resource):
    @jwt_required()
    @auth_namespace.marshal_with(get_user_serializer)
    def get(self,pk):

        user = User.get_by_id(pk)

        return user, HTTPStatus.OK
    

    @jwt_required()
    def delete(self, pk):
        user = User.get_by_id(pk)

        user.delete()

        return {"message":f"User with id {pk} has been deleted"}, HTTPStatus.OK


@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)


        return {'access_token': access_token}, HTTPStatus.OK