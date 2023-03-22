from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from api.utils import db
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
        'teacher': fields.String(
            description='Teacher assigned to course',
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
    
    @course_namespace.expect(course_serializer)
    @course_namespace.marshal_with(course_serializer)
    def post(self):
        """
        Create a new course
        """

        data = course_namespace.payload
        
        new_course = Course(
            id = data['id'],
            name = data['name'],
            teacher = data['teacher']

        )
        
        new_course.save()


        return new_course, HTTPStatus.CREATED
