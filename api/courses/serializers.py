from flask_restx import Namespace, fields

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
    'StudentCourseCreate',
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
            description='Name of teacher assigned to course',
            required = True
    ),
    'student_id':fields.String(
            description='ID of student registering for course',
            required = True
    ),
    'student_name':fields.String(
            description='Name of student registering for course',
            required = True
    )
    

    }
)


get_course_students_serializer = course_namespace.model(
    'CourseStudentsGet',
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
            description='Name of teacher assigned to course',
            required = True
    ),
    'students':fields.String(
            description='ID of student registering for course',
            required = True
    )
    

    }
)
