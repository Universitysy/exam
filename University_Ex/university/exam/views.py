from django.shortcuts import render
from .models import Teacher

def home(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers

        }
    return render(request, 'pages/index.html', context)


def login(request):
     return render(request, 'login/login.html', {})