from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from api.utils import db
from ..students.models import Student
from ..students.mixins import StudentResponseMixin
from .models import Course
from .mixins import CourseResponseMixin
from .serializers import (
    course_serializer, register_course_serializer, 
    get_student_course_serializer, get_course_students_serializer
)


from flask_restx import Namespace, Resource

course_namespace = Namespace(
    'courses',
    description='a namespace for course logic')

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
    @jwt_required()
    @course_namespace.marshal_with(course_serializer)
    def get(self, course_id):
        """
        Get a course by id
        """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK
    
    @jwt_required()
    @course_namespace.expect(course_serializer)
    @course_namespace.marshal_with(course_serializer)
    def put(self, course_id):

        course = Course.get_by_id(course_id)
        data = course_namespace.payload

        for key, value in data.items():
            course[key] = value

        db.session.commit()
        
    
        return course, HTTPStatus.OK
    
    @jwt_required()
    def delete(self, course_id):
        course = Course.get_by_id(course_id)
        course.delete()

        return {"message":f"Course with id {course_id} has been deleted"}, HTTPStatus.OK


@course_namespace.route('/register')
class StudentCourseCreate(Resource):
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
        response['student_id'] = student_id
        response['student_name'] = student.user.get_full_name()
        response['course_id'] = course_id
        response['course_name'] = course.name
        response['teacher'] = course.teacher
    
        return response, 201
    
@course_namespace.route('/<int:course_id>/students')
class StudentCourseStudentsGet(Resource, StudentResponseMixin):
    @jwt_required()
    @course_namespace.marshal_with(get_course_students_serializer)
    def get(self, course_id):
        """
        Get all students registered to a course
        """
        course = Course.get_by_id(course_id)
        students = course.students

        response = {}
        response['course_id'] = course_id
        response['course_name'] = course.name
        response['teacher'] = course.teacher

        student_response = []
        for student in students:
            student_response.append(self.get_student_response(student))

        response['students'] = student_response
    
        return response, 201

        


