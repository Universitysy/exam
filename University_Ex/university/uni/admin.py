from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        list_display = ['username']

class StudentAdmin(ImportExportModelAdmin):
    class Meta:
        model = Student
        list_display=['username']



class TeacherAdmin(ImportExportModelAdmin):
    class Meta:
        model = Teacher
        list_display=['username']

class AdminAdmin(ImportExportModelAdmin):
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

class Selected_Exam_Admin(admin.ModelAdmin):
    class Meta:
        model = Selected_exam
        


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Exam_Swap_Request, Exam_Swap_Request_Admin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Exam_Registration, Exam_RegistrationAdmin)
admin.site.register(Teacher_Availability, Teacher_Availability_Admin)
admin.site.register(Selected_exam, Selected_Exam_Admin)


