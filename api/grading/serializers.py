from flask_restx import Namespace, fields

from .models import GradePoints

grading_namespace = Namespace(
    'grading',
    description='a namespace for grading logic')


student_course_grade_serializer = grading_namespace.model(
    'StudentCourseGrade',
    {
        'student_id':fields.String(
            description='ID of associated student',
            required = True
        ),
        'course_id':fields.Integer(
            description='ID of course grade is assigned to',
            required = True
        ),
        'score': fields.Float(
            description='score attained by student for course',
            required = True
        ),
        'grade_point': fields.String(
            description='associated grade point for score attained',
            required = True,
            enum = GradePoints
        ),
    }

)


student_gpa_serializer = grading_namespace.model(
    'StudentGPA',
    {
    'student_id':fields.String(
            description='ID of associated student',
            required = True
        ),

    'student_name':fields.String(
            description='name of associated student',
            required = True
        ),

    'gpa':fields.Float(
            description='gpa of associated student',
            required = True
        )
    }
    
)