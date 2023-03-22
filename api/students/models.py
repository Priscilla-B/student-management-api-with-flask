from api.utils import db
from api.courses.models import StudentCourse
from sqlalchemy.sql import func

class Student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.String(20),primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    courses = db.relationship('Course', secondary=StudentCourse)
    
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
    
    @classmethod
    def get_by_id(cls, student_id):
        return cls.query.get_or_404(student_id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()