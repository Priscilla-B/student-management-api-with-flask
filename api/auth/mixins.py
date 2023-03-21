from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Role

class UserCreationMixin(object):

    @classmethod
    def create_user(self, data, role_name):

        new_user = User(
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                username = data.get('username'),
                email = data.get('email'),
                password = generate_password_hash(data.get('password'))
            )
        
        try:
            role = Role.query.filter_by(name=role_name).first()
        except:
            role = Role(name=role_name)
            role.save()
        
        # admin is default role but will be changed 
        # based on where mixin is called from

        new_user.role = [role]

        new_user.save()

        return new_user
    
