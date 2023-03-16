import os
from decouple import config
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# get the directory of file being edited

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #  prevent sql alchemy from setting up a session to 
    # track inserts, updates, and deletes for models
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # to log queries generated

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass


config_dict = {
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}