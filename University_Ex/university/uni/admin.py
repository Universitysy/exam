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

class Student_user_Admin(admin.ModelAdmin):
    class Meta:
        model = Student_user
        list_display=['username']

class Teacher_user_Admin(admin.ModelAdmin):
    class Meta:
        model = Teacher_user
        list_display=['username']

class Admin_user_Admin(admin.ModelAdmin):
    class Meta:
        model = Admin_user
        list_display=['username']


class TeacherAdmin(admin.ModelAdmin):
    class Meta:
        model = Teacher
        list_display=['username']

class AdminAdmin(admin.ModelAdmin):
    class Meta:
        model = Admin
        list_display=['username']

class Exam_Swap_Request_Admin(admin.ModelAdmin):
    class Meta:
        model = Exam_Swap_Request
        list_display=['status']

class RoomAdmin(admin.ModelAdmin):
    class Meta:
        model = Room
        list_display=['location']

class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course
        list_display=['name']

class ExamAdmin(admin.ModelAdmin):
    class Meta:
        model = Exam
        list_display=['date']


class Exam_RegistrationAdmin(admin.ModelAdmin):
    class Meta:
        model = Exam_Registration
        list_display=['student_number']

class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course
        list_display=['name']


class Teacher_Availability_Admin(admin.ModelAdmin):
    class Meta:
        model = Teacher_Availability
        


admin.site.register(User, UserAdmin)
admin.site.register(Teacher_user, Teacher_user_Admin)
admin.site.register(Student_user, Student_user_Admin)
admin.site.register(Admin_user, Admin_user_Admin)
admin.site.register(Exam_Swap_Request, Exam_Swap_Request_Admin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Exam_Registration, Exam_RegistrationAdmin)
admin.site.register(Teacher_Availability, Teacher_Availability_Admin)


