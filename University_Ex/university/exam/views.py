from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .Form import *
import traceback
from django.contrib.auth.hashers import make_password
import secrets


def teacher_path(request):
   
    return render(request, 'pages/teachers.html', )

def room_path(request):
    return render(request, 'pages/room.html')

def contact_path(request):
    return render(request, 'pages/contactUs.html')

def assi_path(request):
    return render(request, 'pages/assignment.html')

    

def home(request):
    
    context = {
        }
    return render(request, 'pages/index.html', context)

def student_home(request):
    user = request.user
    return render(request, 'student_home.html', {'user':user})
    
def teacher_home(request):
    user = request.user
    return render(request, 'teacher_home.html', {'user':user})

def admin_home(request):
    user = request.user
    return render(request, 'admin_home.html', {'user':user})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'STUDENT':
                return redirect('student_home')
            elif user.role == 'TEACHER':
                return redirect('teacher_home')
            elif user.role == 'ADMIN':
                return redirect('admins_home')
                
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login/login.html', {'error_message': error_message})
    else:
        return render(request, 'login/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


def add_teacher(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = 'admin'

        check_email = User.objects.filter(email=email)

        if check_email :
            return render(request, 'pages/manageTeacher.html', { 'teachers': teachers, 'error': 'this email has been taken, use your own email!'})
        else:


            teacher = Teacher.objects.create_user(username = username,
                                                  first_name= first_name,
                                                  last_name=last_name,
                                                  email = email,
                                                  password = password,
                                                  role='TEACHER')

            teacher.save()
            return render(request, 'pages/manageTeacher.html', {'teachers': teachers})
        
    else:
        return render(request, 'pages/manageTeacher.html', {'teachers': teachers})
   


def add_student(request):
    students = Student.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = 'admin'

        check_email = User.objects.filter(email=email)

        if check_email :
            return render(request, 'pages/manageStudent.html', {'students': students, 'error': 'this email has been taken use your own email!'})
        else:

            teacher = Teacher.objects.create_user(username = username,
                                                  first_name= first_name,
                                                  last_name=last_name,
                                                  email = email,
                                                  password = password,
                                                  role='STUDENT')

            student.save()
            return render(request, 'pages/manageStudent.html', {'students': students})
        
    else:
        return render(request, 'pages/manageStudent.html', {'students': students})
    pass

def remove_student(request, student_id):
    student = Student.student.get(id=student_id)
    student.delete()
    return redirect(reverse('add_student'))


def remove_teacher(request, teacher_id):
    teacher = Teacher.teacher.get(id=teacher_id)
    teacher.delete()
    return redirect(reverse('add_teacher'))




