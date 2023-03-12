from utils import db
from sqlalchemy.sql import func

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    teacher = db.relationship(db.String(150), nullable=False)
    students = db.relationship('Student', backref='course')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   

    
    def __repr__(self):
        return f'{self.username}'