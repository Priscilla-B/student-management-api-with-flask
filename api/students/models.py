from api.utils import db
from sqlalchemy.sql import func

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f'{self.username}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()