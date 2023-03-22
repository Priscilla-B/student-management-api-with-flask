
class StudentResponseMixin(object):

    def get_response(self, student_instance):
        
        response_data = {}
        user = student_instance.user.as_dict()
        user['student_id'] = student_instance.student_id
        user['user_id'] = user['id']
        response_data.update(user)

        return response_data