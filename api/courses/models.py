from sqlalchemy.sql import func

from api.utils import db


StudentCourse = db.Table(
    'student_course', db.Model.metadata,
    db.Column('student_id', db.String(20), db.ForeignKey('student.student_id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    teacher= db.Column(db.Integer, db.ForeignKey('user.id'))
    # students = db.relationship('Student', secondary=StudentCourse)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   

    
    def __repr__(self):
        return f'{self.username}'