from utils import db
from sqlalchemy.sql import func

class Teacher(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    teacher_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f'{self.username}'