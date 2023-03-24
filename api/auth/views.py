from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, get_jwt_identity)
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash

from api.utils import db
from .models import User, RoleOptions
from .mixins import UserCreationMixin
from .serializers import register_serializer, login_serializer, get_user_serializer

auth_namespace = Namespace(
    'auth',
    description='a namespace for authentication logic')




@auth_namespace.route('/register')
class Register(Resource, UserCreationMixin):

    @auth_namespace.expect(register_serializer)
    # @auth_namespace.marshal_with(register_serializer)
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()
       
        return self.create_user(data)
        
    
    

@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_serializer)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user is None:
            response = {"message": "User with email {email} could not be found"}
            return response, 400
        
        if not check_password_hash(user.password, password):
            response =  {"message": "Password incorrect"}
            http_status = 400
        else:
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            http_status = 201

        return response, http_status
       
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
    @auth_namespace.expect(get_user_serializer)
    @auth_namespace.marshal_with(get_user_serializer)
    def put(self, pk):

        user = User.get_by_id(pk)
        data = auth_namespace.payload
        user_fields = [c.name for c in User.__table__.columns]

        for key, value in data.items():
            if key in user_fields:
                user[key] = value
            else:
                return {"msg":f"Could not update student with key {key}"}, HTTPStatus.BAD_REQUEST
        
        db.session.commit()
        
    
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