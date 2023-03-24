from flask_restx import Namespace, Resource, fields
from .models import RoleOptions


auth_namespace = Namespace(
    'auth',
    description='a namespace for authentication logic')

register_admin_serializer = auth_namespace.model(
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

create_user_serializer = auth_namespace.model(
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
                            enum=RoleOptions
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
        'role':fields.String(required=True, 
                            decription='role for user, whether staff or admin.',
                            enum=RoleOptions
                                  )        
    }
)
