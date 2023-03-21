from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from api.auth.models import User, Role
from api.auth.mixins import UserCreationMixin
from api.utils import db
from .models import Student
from .mixins import StudentResponseMixin

student_namespace = Namespace(
    'students',
    description='a namespace for student logic')


student_serializer = student_namespace.model(
    'Student', 
        {
        'user_id':fields.Integer(
            description='ID of related user',
            required = True
        ),
        'student_id':fields.String(
            description='custom created student ID',
            required = True
        ),
        'first_name': fields.String(
            description='student first name',
            required = True
        ),
        'last_name': fields.String(
            description='student last name',
            required = True
        ),
        'username': fields.String(
            description='username of student in app',
            required = True
        ),
        'email': fields.String(
            description='student email',
            required = True
        )
        }
)


@student_namespace.route('')
class StudentGetCreate(
    Resource, UserCreationMixin, StudentResponseMixin):

    @student_namespace.marshal_with(student_serializer)
    @jwt_required()
    def get(self):
        """
        Get all students
        """

        students = Student.query.all()
        response_data = []
        for student in students:
            response_data.append(self.get_response(student))
    
        return response_data, HTTPStatus.OK
    
    @student_namespace.expect(student_serializer)
    @student_namespace.marshal_with(student_serializer)
    def post(self):
        """
        Create a new student
        """

        data = student_namespace.payload
        
        role_name = 'student'
        new_user = self.create_user(data, role_name).as_dict()

        new_student = Student(
            user_id = new_user['id'],
            student_id = data['student_id']

        )
        
        new_student.save()

        response_data = self.get_response(new_student)
       

        return response_data, HTTPStatus.CREATED


@student_namespace.route('/<student_id>')
class GetUpdateDeleteStudent(Resource, StudentResponseMixin):

    @jwt_required()
    @student_namespace.marshal_with(student_serializer)
    def get(self, student_id):
        student = Student.get_by_id(student_id)
        
        response_data = self.get_response(student)
        return response_data, HTTPStatus.OK
    
    @jwt_required()
    @student_namespace.expect(student_serializer)
    @student_namespace.marshal_with(student_serializer)
    def put(self, student_id):

        student = Student.get_by_id(student_id)
        user = student.user
        data = student_namespace.payload
        student_fields = [c.name for c in Student.__table__.columns]
        user_fields = [c.name for c in User.__table__.columns]

        for key, value in data.items():
            if key in user_fields:
                user[key] = value
    
            elif key in student_fields:
                student[key] = value
            
            else:
                return {"msg":f"Could not update student with key {key}"}, HTTPStatus.BAD_REQUEST
        
        db.session.commit()
        
    
        return self.get_response(student), HTTPStatus.OK
    
    @jwt_required()
    def delete(self, student_id):
        student = Student.get_by_id(student_id)
        user = student.user

        user.delete()

        student.delete()
        return {"message":f"Student with id {student_id} has been deleted"}, HTTPStatus.OK
