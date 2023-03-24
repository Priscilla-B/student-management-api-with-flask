from sqlalchemy.sql import func

from api.utils import db


StudentCourse = db.Table(
    'student_course', db.Model.metadata,
    db.Column('student_id', db.String(20), db.ForeignKey('student.student_id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.relationship('User', backref='teacher')
    students = db.relationship('Student', secondary=StudentCourse, viewonly=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   
    def __repr__(self):
        return f'{self.name}'
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
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
    def get_by_id(cls, course_id):
        return cls.query.get_or_404(course_id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()