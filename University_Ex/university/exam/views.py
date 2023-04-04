from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .Form import *
import traceback
from django.contrib.auth.hashers import make_password
import secrets


def teacher_path(request):
    return render(request, 'pages/teachers.html')

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



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.role == CustomUser.Role.ADMIN:
                return redirect('admins_home')
            elif user.role == CustomUser.Role.STUDENT:
                return redirect('student_home')
            elif user.role == CustomUser.Role.TEACHER:
                return redirect('teacher_home')
        else:
            return render(request, 'login/login.html', {'error': 'Invalid email or password'})
    return render(request, 'login/login.html')



    


def logoutUser(request):
    logout(request)
    return redirect('login')


def add_teacher(request):
    teachers = Teacher.teacher.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = secrets.token_hex(8)

        check_email = CustomUser.objects.filter(email=email)

        if check_email :
            return render(request, 'pages/manageTeacher.html', { 'teachers': teachers, 'error': 'this email has been taken, use your own email!'})
        else:

            teacher = Teacher()
            teacher.username = username
            teacher.first_name =  first_name
            teacher.last_name = last_name
            teacher.email =  email
            teacher.password = password
            teacher.role = Teacher.base_role

            teacher.save()
            return render(request, 'pages/manageTeacher.html', {'teachers': teachers})
        
    else:
        return render(request, 'pages/manageTeacher.html', {'teachers': teachers})


def add_student(request):
    students = Student.student.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = secrets.token_hex(8)

        check_email = CustomUser.objects.filter(email=email)

        if check_email :
            return render(request, 'pages/manageStudent.html', {'students': students, 'error': 'this email has been taken use your own email!'})
        else:

            student = Student()

            student.username = username
            student.first_name = first_name
            student.last_name = last_name
            student.email = email
            student.password = password
            student.role = Student.base_role

            student.save()
            return render(request, 'pages/manageStudent.html', {'students': students})
        
    else:
        return render(request, 'pages/manageStudent.html', {'students': students})


def remove_student(request, student_id):
    student = Student.student.get(id=student_id)
    student.delete()
    return redirect(reverse('add_student'))


def remove_teacher(request, teacher_id):
    teacher = Teacher.teacher.get(id=teacher_id)
    teacher.delete()
    return redirect(reverse('add_teacher'))




