from flask_restx import  fields

create_student_serializer = {
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
        ),
        'password': fields.String(
            description='password to student account',
            required = True
        )
}



student_serializer = {
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
