from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('', home, name='student_home' ),
    path('', home, name='admin_home' ),
    path('', home, name='teacher_home' ),
    
    path('login/', login_view, name='login' ),
    path('addteacher/', add_teacher, name='add_teacher'),
    path('addstudent/', add_student, name='add_student'),
]