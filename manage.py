import getpass

from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from api.auth.models import User
from app import app

cli = FlaskGroup(app)


@cli.command('create_admin')
def create_admin():
    """
    Creates an admin user from cli
    """
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    username = input("Enter username: ")
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1

    
    try:
        user = User(
            first_name=first_name,
            last_name=last_name, 
            username=username,  
            email=email,
            password=generate_password_hash(password),
            is_staff=True,
            is_active=True,
            role='admin'
        )
        
        user.save()
        
        
    except Exception:
        print(Exception)


if __name__ == "__main__":
    cli()  

     