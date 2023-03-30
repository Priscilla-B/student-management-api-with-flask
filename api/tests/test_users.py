import unittest

from .. import create_app
from ..config.config import config_dict
from ..utils import db


class UserTestCase(unittest.TestCase):
    def setup(self):
        self.app = create_app(config=config_dict['test'])
        self.app_contxt = self.app.app_context()
        self.app_contxt.push()
        self.client = self.app.test_client()
        
        db.create_all()

    def teardown(self):
        """
        Destroys database  and removes app context after running tests
        """
        db.drop_all()

        self.app_contxt.pop()
        self.app = None
        self.client = None