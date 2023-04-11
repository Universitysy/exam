from django.shortcuts import redirect
from .models import User

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Redirect to the appropriate URL if the user tries to go back to the login page
        if request.path == '/' and request.user.is_authenticated:
            if request.user.role == User.Role.ADMIN:
                return redirect('admins_home')
            elif request.user.role == User.Role.TEACHER:
                return redirect('teacher_home')
            else:
                return redirect('student_home')


        return response
