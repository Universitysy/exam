from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('student/', home, name='student_home' ),
    path('admin/', home, name='admins_home' ),
    path('teacher/', home, name='teacher_home' ),
    
    path('', login_view, name='login' ),
    path('addteacher/', add_teacher, name='add_teacher'),
    path('addstudent/', add_student, name='add_student'),

    path('teacherS/', teacher_path, name='teacher_path'),
    path('contactUs/', contact_path, name='contact_path'),
    path('room/', room_path, name='room_path'),
    path('assignements/', assi_path, name='assi_path'),
]