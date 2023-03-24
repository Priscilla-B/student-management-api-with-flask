from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from api.utils import db
from ..students.models import Student
from .models import Course
from .mixins import CourseResponseMixin



from flask_restx import Namespace, Resource

course_namespace = Namespace(
    'courses',
    description='a namespace for course logic')


course_serializer = course_namespace.model(
    'Course', 
        {
        'id':fields.Integer(
            description='ID of course',
            required = True
        ),
        'name':fields.String(
            description='Name of course',
            required = True
        ),
        'teacher_id': fields.Integer(
            description='Teacher assigned to course',
            required = True
        )
        }
)


register_course_serializer = course_namespace.model(
    'StudentCourse',
    {
    'student_id':fields.String(
            description='ID of student registering for course',
            required = True
    ),
    'course_id':fields.Integer(
            description='ID of course being taken',
            required = True
    )

    }
)


get_student_course_serializer = course_namespace.model(
    'StudentCourseGet',
    {
    'course_id':fields.Integer(
            description='ID of course being taken',
            required = True
    ),
    'course_name':fields.String(
            description='Name of course',
            required = True
    ),
    'teacher':fields.String(
            description='Name of course',
            required = True
    ),
    'student_id':fields.String(
            description='ID of student registering for course',
            required = True
    ),
    'student_name':fields.String(
            description='Name of course',
            required = True
    )
    

    }
)


@course_namespace.route('')
class CourseGetCreate(Resource):

    @course_namespace.marshal_with(course_serializer)
    @jwt_required()
    def get(self):
        """
        Get all courses
        """

        courses = Course.query.all()
    
        return courses, HTTPStatus.OK
    
    @jwt_required()
    @course_namespace.expect(course_serializer)
    @course_namespace.marshal_with(course_serializer)
    def post(self):
        """
        Create a new course
        """

        data = course_namespace.payload
        
        new_course = Course(
            name = data['name'],
            teacher_id = data['teacher_id']

        )
        
        new_course.save()


        return new_course, HTTPStatus.CREATED


@course_namespace.route('/<int:course_id>')
class GetUpdateDeleteCourse(Resource):
    def get(self):
        """
        Get details of a course
        """


@course_namespace.route('/register')
class StudentCourseGetCreate(Resource):
    @jwt_required()
    @course_namespace.expect(register_course_serializer)
    @course_namespace.marshal_with(get_student_course_serializer)
    def post(self):
        """
        Register a student to a course
        """
        data = course_namespace.payload
        student_id = data['student_id']
        course_id = data['course_id']

        student = Student.get_by_id(student_id)
        course = Course.get_by_id(course_id)
        student.courses.append(course)
        db.session.commit()

        response = {}
        response['course_id'] = course_id
        response['course_name'] = course.name
        response['teacher'] = course.teacher
        response['student_id'] = student_id
        response['student_name'] = student.user.get_full_name()

        return response, 201

        


