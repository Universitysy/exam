from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser
        list_display = ['username']

class StudentAdmin(admin.ModelAdmin):
    class Meta:
        model = Student
        list_display=['username']


class TeacherAdmin(admin.ModelAdmin):
    class Meta:
        model = Teacher
        list_display=['username']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)


