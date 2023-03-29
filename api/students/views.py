from flask_restx import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from ..auth.models import User
from ..auth.views import create_user_model
from ..auth.mixins import UserCreationMixin
from ..utils import db
from ..utils.decorators import admin_required
from .models import Student
from .mixins import StudentResponseMixin
from .serializers import *

student_namespace = Namespace(
    'students',
    description='a namespace for student logic')

create_student_model = student_namespace.model(
    'Student', create_student_serializer)

student_model= student_namespace.model(
    'StudentGet', student_serializer)

@student_namespace.route('')
class StudentGetCreate(
    Resource, UserCreationMixin, StudentResponseMixin):

    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self):
        """
        Get all students
        """

        students = Student.query.all()
        response_data = []
        for student in students:

            student_response = marshal(self.get_student_response(student), student_model)
            response_data.append(student_response)
    
        return response_data, HTTPStatus.OK
    
    @jwt_required()
    @admin_required()
    @student_namespace.expect(create_student_model)
    def post(self):
        """
        Create a new student
        """

        data = student_namespace.payload
        data['role'] = 'student'
        

        user_response = self.create_user(data)
        if user_response[1] == 201:
            new_user = marshal(user_response[0], create_user_model)
        else:
            return user_response
       

        new_student = Student(
            user_id = new_user['id'],
            student_id = data['student_id']

        )
        
        new_student.save()

        student_response = marshal(self.get_student_response(new_student), student_model)

        return student_response, HTTPStatus.CREATED


@student_namespace.route('/<student_id>')
class GetUpdateDeleteStudent(Resource, StudentResponseMixin):

    @jwt_required()
    @student_namespace.marshal_with(student_model)
    def get(self, student_id):
        """
        Get details of a student with given id
        """
        student = Student.get_by_id(student_id)
        
        student_response = marshal(self.get_student_response(student), student_model)
        return student_response, HTTPStatus.OK
    
    @jwt_required()
    @admin_required()
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    def put(self, student_id):
        """
        Update a student with given id
        """

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
        
        student_response = marshal(self.get_student_response(student), student_model)
    
        return student_response, HTTPStatus.OK
    
    @jwt_required()
    @admin_required()
    def delete(self, student_id):
        """
        Update a student with given id
        """
        student = Student.get_by_id(student_id)
        user = student.user

        user.delete()

        student.delete()
        return {"message":f"Student with id {student_id} has been deleted"}, HTTPStatus.OK
