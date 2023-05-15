from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('student/', home, name='student_home' ),
    path('myadmin/', home, name='admins_home' ),
    path('teacher/', home, name='teacher_home' ),
    path('', home, name='home' ),
    
    path('login/', login_view, name='login' ),
    path('logout/', logout_view , name='logout' ),
    path('addteacher/', add_teacher, name='add_teacher'),
    path('addstudent/', add_student, name='add_student'),
    path('Exam/', add_exam, name='add_exam'),
    path('displayExam/', list_of_exams, name='display_exam'),
    path('alltime/', teachers_time, name='all_time'),
    path('delltime/', delete_selected_exam , name='delete_selected_exam'),
    path('addtime/', select_preferred_time , name='add_time'),
    path('room/', display_rooms, name='rooms'),
    path('teacherS/', teacher_path, name='teacher_path'),
    path('contactUs/', contact_path, name='contact_path'),
    path('assignements/', assi_path, name='assi_path'),


]