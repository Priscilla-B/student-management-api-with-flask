from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from api.auth.models import User, Role
from api.auth.mixins import UserCreationMixin
from api.utils import db
from .models import Student

student_namespace = Namespace(
    'students',
    description='a namespace for student logic')


get_student_serializer = student_namespace.model(
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

create_student_serializer = student_namespace.model(
    'Student', 
        {
        'user_id':fields.Integer(
            description='ID of related user',
            required = True
        ),
        'student_id':fields.String(
            description='custom created student ID',
            required = True
        )
        }
)

@student_namespace.route('/students')
class StudentGetCreate(Resource):

    @student_namespace.marshal_with(get_student_serializer)
    @jwt_required()
    def get(self):
        """
        Get all students
        """

        students = Student.query.all()
        return students, HTTPStatus.OK
    
    @student_namespace.expect(create_student_serializer)
    @student_namespace.marshal_with(create_student_serializer)
    def post(self):
        """
        Create a new student
        """

        data = student_namespace.payload
        
        role_name = 'student'
        new_user = self.create_user(data, role_name).as_dict()

        new_student = Student(
            user_id = data['user_id'],
            student_id = data['student_id']

        )

        try:
            role = Role.query.get(name='student').first()
        except:
            role = Role(name='student')
            role.save()
        
        new_student.user.role = [role]
        new_student.save()

        return new_student, HTTPStatus.CREATED


@student_namespace.route('/student/<student_id>')
class GetUpdateDeleteStudent(Resource):

    @jwt_required()
    @student_namespace.marshal_with(get_student_serializer)
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first_or_404()

        return student, HTTPStatus.OK
