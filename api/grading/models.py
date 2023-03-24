from enum import Enum

from api.utils import db
from sqlalchemy.sql import func

class GradePoints(Enum):
    A = 4
    B = 3
    C = 2
    D = 1
    F = 0


class Grade(db.Model):
    __tablename__ = 'grade'

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='course')
    student_id = db.Column(db.String(20), db.ForeignKey('student.student_id'), nullable=False)
    student = db.relationship('Student', backref='student')
    score = db.Column(db.Float(), nullable=False)
    grade_point = db.Column(db.Enum(GradePoints), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f'{self.student_id}'
    
    def __getitem__(self, key):
        """
        To enable item assignments such as user["name"]
        instead of user.name
        """
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        """
        To enable item assignments such as student["name"]="new name{}
        instead of student.name = "new name"
        """
        return setattr(self, key, value)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()