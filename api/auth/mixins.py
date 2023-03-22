from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

class UserCreationMixin(object):

    @classmethod
    def create_user(self, data, role):

        new_user = User(
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                username = data.get('username'),
                email = data.get('email'),
                password = generate_password_hash(data.get('password')),
                role=role
            )
    

        new_user.save()

        return new_user
    
