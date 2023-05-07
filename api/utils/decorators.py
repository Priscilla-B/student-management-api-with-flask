from ..auth.models import User, RoleOptions
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from http import HTTPStatus

# Get the role of authenticated user
def get_user_role(id:int):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.role
    else:
        return None


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role']=='admin':
                return fn(*args, **kwargs)
            if get_user_role(claims['sub']) == RoleOptions.admin:
                return fn(*args, **kwargs)
            else:
                return {"message": "Administrator access required"}, 401
        return decorator
    return wrapper