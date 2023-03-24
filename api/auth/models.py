from enum import Enum
from sqlalchemy.sql import func

from api.utils import db



class RoleOptions(Enum):
    admin = 'admin'
    student = 'student'
    teacher = 'teacher'



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
    courses = db.relationship('Course', backref='user')
    # uselist=False makes relationship One to One
    role = db.Column(db.Enum(RoleOptions), nullable=True)
    
    def __repr__(self):
        return f'{self.username}'
    
    def __getitem__(self, key):
        """
        To enable item assignments such as user["name"]
        instead of user.name
        """
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        """
        To enable item re-assignments such as user["name"] = "new name"
        instead of user.name = "new name"
        """
        return setattr(self, key, value)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def get_by_id(cls, student_id):
        return cls.query.get_or_404(student_id)
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

