from enum import Enum

from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin
from sqlalchemy.sql import func

from api.utils import db



# class RoleOptions(Enum):
#     ADMIN = 'admin'
#     STUDENT = 'student'
#     TEACHER = 'teacher'


UserRole = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    student = db.relationship('Student', backref='user', uselist=False)
    # uselist=False makes relationship One to One
    role = db.relationship('Role', secondary=UserRole)
    
    def __repr__(self):
        return f'{self.username}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


    def __repr__(self):
        return f'{self.name}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

