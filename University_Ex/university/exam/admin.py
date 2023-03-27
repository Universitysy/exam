from django.contrib import admin
from .models import *

class TeacherAdmin(admin.ModelAdmin):
    class Meta:
        model = Teacher
        list_display = ['get_full_name']

class StudentAdmin(admin.ModelAdmin):
    class Meta:
        model = Student
        list_display = ['get_full_name']


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
