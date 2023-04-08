from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        list_display = ['username']

class StudentAdmin(admin.ModelAdmin):
    class Meta:
        model = Student
        list_display=['username']


class TeacherAdmin(admin.ModelAdmin):
    class Meta:
        model = Teacher
        list_display=['username']

class AdminAdmin(admin.ModelAdmin):
    class Meta:
        model = Admin
        list_display=['username']


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)


