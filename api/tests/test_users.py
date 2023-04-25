import unittest
from werkzeug.security import generate_password_hash

from .. import create_app
from ..config.config import config_dict
from ..auth.models import User
from ..utils import db



class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.app_contxt = self.app.app_context()
        self.app_contxt.push()
        self.client = self.app.test_client()
        
        db.create_all()

    def tearDown(self):
        """
        Destroys database  and removes app context after running tests
        """
        db.drop_all()

        self.app_contxt.pop()
        self.app = None
        self.client = None


    def test_user_creation(self):
        data = {
            "first_name":"Test",
            "last_name":"User",
            "username":"test_user",
            "email":"test_user@gmail.com",
            "password":"test123@",
            "role":"teacher"
        }

        response = self.client.post('/auth/create_user', json=data)

        user = User.query.filter_by(email=data["email"]).first()
        assert user.username == data["username"]

        assert response.status_code == 201

    def test_login(self):
        data = {
            "email":"test_user@gmail.com",
            "password":"test123@"
        }
        response = self.client.post('/auth/login', json=data)

        assert response.status_code != 200
        # user should not exist in database, so login should not be possible