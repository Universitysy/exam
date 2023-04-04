from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('student/', home, name='student_home' ),
    path('admin/', home, name='admins_home' ),
    path('teacher/', home, name='teacher_home' ),
    
    path('login/', login_view, name='login' ),
    path('addteacher/', add_teacher, name='add_teacher'),
    path('addstudent/', add_student, name='add_student'),
]