from flask_restx import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from ..students.models import Student
from .models import Grade
from .serializers import *

grading_namespace = Namespace(
    'grading',
    description='a namespace for grading logic')


@grading_namespace.route('')
class CreateStudentGrade(Resource):

    @jwt_required()
    @grading_namespace.expect(student_course_grade_serializer)
    @grading_namespace.marshal_with(student_course_grade_serializer)
    def post(self):
        data = grading_namespace.payload

        new_grade = Grade(
            student_id = data['student_id'],
            course_id = data['course_id'],
            score = data['score'],
            grade_point = data['grade_point']
        )

        new_grade.save()
        return new_grade, HTTPStatus.CREATED


@grading_namespace.route('/gpa/<student_id>')
class GetStudentGPA(Resource):

    @jwt_required()
    def get(self, student_id):
        student = Student.get_by_id(student_id)
        courses = student.courses
        if not courses:
            return {"message": "student_not registered to any course"}

        grade_points = []
        
        for course in courses:
            grade = Grade.query.filter_by(
                student_id=student_id,
                course_id = course.id
            ).first()
            if grade:
                grade_point = grade.grade_point.value
                grade_points.append(grade_point)

        if grade_points:
            gpa = sum(grade_points)/len(grade_points)
        else:
            return {"message": "No exists grade for associated student"}

        
        response_data = {
            "student_id": student_id,
            "student_name": student.user.get_full_name(),
            "gpa": gpa
        }
        return marshal(response_data, student_gpa_serializer), HTTPStatus.OK   