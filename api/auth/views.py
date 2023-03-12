from flask_restx import Namespace, Resource

auth_namespace = Namespace(
    'auth',
    description='a namespace for authentication logic')