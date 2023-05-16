from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .Form import *
import traceback
from django.contrib.auth.hashers import make_password
import secrets
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .utils import TeacherCalendar
from .utils import AdminCalendar


def teacher_path(request):
   
    return render(request, 'pages/teachers.html', )


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
    return render(request, 'pages/login_student.html', {'user':user})
    
def teacher_home(request):
    user = request.user
    return render(request, 'pages/login_teacher.html', {'user':user})

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
                return render(request, 'pages/login_student.html')
            elif user.role == 'TEACHER':
                return render(request, 'pages/login_teacher.html')
            elif user.role == 'ADMIN':
                return redirect('admins_home')
                
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login/login.html', {'error_message': error_message})
    else:
        return render(request, 'login/login.html')



def logout_view(request):
    logout(request)
    return redirect('home')


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

            student = Student.objects.create_user(username = username,
                                                  first_name= first_name,
                                                  last_name=last_name,
                                                  email = email,
                                                  password = password,
                                                  role='STUDENT')

            student.save()
            return render(request, 'pages/manageStudent.html', {'students': students})
        
    else:
        return render(request, 'pages/manageStudent.html', {'students': students})
    

def remove_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect(reverse('add_student'))


def remove_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.delete()
    return redirect(reverse('add_teacher'))



def add_exam(request):
    exams = Exam.objects.all()
    courses = Course.objects.all()
    rooms = Room.objects.all()

    context = { 'exams': exams,
                'courses': courses,
                'rooms': rooms}

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        assigned_room = Room.objects.get(name=request.POST.get('assigned_room'))
        course_exam = Course.objects.get(name=request.POST.get('course_exam'))

        exam = Exam.objects.create(start_time=start_time,
                                   end_time=end_time,
                                   date=date,
                                   assigned_room=assigned_room,
                                   course_exam=course_exam)
        exam.save()
        return render(request, 'pages/exam.html', context)
    else:
        return render(request, 'pages/exam.html', context)



def delete_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    exam.delete()
    return redirect(reverse('add_teacher'))

    
def list_of_exams(request, year=None , month=None):
    teacher = request.user
    teacher_availability = Teacher_Availability.objects.filter(teacher_av=teacher)
    selected_exams = Selected_exam.objects.filter(t_a__in=teacher_availability)
    exams = Exam.objects.all()

  
    if year and month:
        year, month = int(year), int(month)
    else:
        now = datetime.now()
        year, month = now.year, now.month
    ##calender
    calendar_html = TeacherCalendar(year, month, teacher).formatmonth()
 

    context = {'exams':exams, 
               'selected_exams':selected_exams,
               'calendar': calendar_html,
               'teacher': teacher,
                }
    return render(request, 'pages/display_exam.html', context)





def select_preferred_time(request):
    if request.method == 'POST':
        exam_ids = request.POST.getlist('preferred_time')
        teacher = request.user

        for exam_id in exam_ids:
            exam = Exam.objects.get(id=exam_id)

            # check if the selected exam has already been added with the same teacher and room
            if Selected_exam.objects.filter(
                    Q(t_a__teacher_av=teacher) & Q(e_x=exam) & Q(e_x__assigned_room= exam.assigned_room)
            ).exists():
                continue

            time_slot = Teacher_Availability.objects.create(
                teacher_av=teacher,
                time_start=exam.start_time,
                time_end=exam.end_time,
                date=exam.date
            )

            selected_exam = Selected_exam.objects.create(t_a=time_slot, e_x=exam)

        messages.success(request, 'Your preferred times have been added successfully.')
        return redirect(reverse('display_exam'))
    else:
        messages.error(request, 'Please select at least one exam.')
        return redirect(reverse('display_exam'))







def teachers_time(request, year=None , month=None):
    # SELECT *
    # FROM selected_exam
    # INNER JOIN teacher_availability ON selected_exam.t_a_id = teacher_availability.id
    # INNER JOIN teacher ON teacher_availability.teacher_av_id = teacher.id;
    selected_exam = Selected_exam.objects.all().select_related('t_a__teacher_av')
    selected_room = Selected_exam.objects.all().select_related('e_x__assigned_room')
    
    teachers = set(se.t_a.teacher_av.username for se in selected_exam)
    rooms = set(sr.e_x.assigned_room.name for sr in selected_room)

    # Create a dictionary where the keys are the room names and the values are the exams assigned to that room
    exams_by_room = {}
    for room in rooms:
        exams_by_room[room] = [se for se in selected_exam if se.e_x.assigned_room.name == room]


    #admin calender
    teacher = request.user
    if year and month:
        year, month = int(year), int(month)
    else:
        now = datetime.now()
        year, month = now.year, now.month
   
    calendar_html = AdminCalendar(year, month, teacher).formatmonth()
 
    context = {
    'teachers': teachers,
    'selected_exam': selected_exam ,
    'exams_by_room': exams_by_room,
    'calendar': calendar_html,
    'teacher': teacher,
    }
    return render(request, 'pages/teachers_time.html', context)







def delete_selected_exam(request):
    if not request.user.role == 'ADMIN':
        return HttpResponseForbidden("You must be an admin to delete selected exams.")

    if request.method == 'POST':
        # Get the IDs of the selected exams
        selected_exam_ids = request.POST.getlist('selected_exam')
        
        # Delete the selected exams
        Selected_exam.objects.filter(id__in=selected_exam_ids).delete()
        
        # Show success message
        messages.success(request, 'Selected exams have been deleted successfully.')
        
        # Redirect to the same page
        return HttpResponseRedirect(reverse('all_time'))








def display_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'pages/room.html', {'rooms':rooms})


def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('courseName')

        course_is_exist = Course.objects.filter(name='name')
        if not course_is_exist :
            course = Course.objects.create(name=name)
            return redirect('add_exam')
        return redirect('add_exam')
    return redirect('add_exam')


def add_room(request):
    if request.method == 'POST':
        name = request.POST.get('roomName')
        max_capacity = request.POST.get('max_capacity')
        is_available = request.POST.get('is_available')

        room_is_exist = Course.objects.filter(name='name')
        if not room_is_exist :
            room = Room.objects.create(name=name, max_capacity=max_capacity, is_available=is_available )
            return redirect('add_exam')
        return redirect('add_exam')
    return redirect('add_exam')

        













