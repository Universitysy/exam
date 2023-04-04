from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Permission
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'

    base_role = Role.ADMIN
    

    

    role = models.CharField(max_length=10, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.STUDENT)


class  Student(CustomUser):
    
    base_role = CustomUser.Role.STUDENT

    student = StudentManager()

    @property
    def get_full_name(self):
        return super().get_full_name

    
    
    class Meta:
        proxy = True


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.TEACHER)

class  Teacher(CustomUser):
    base_role = CustomUser.Role.TEACHER

    teacher = TeacherManager()

    def get_full_name(self):
        return super().get_full_name
    
    class Meta:
        proxy = True






class Request_t(models.Model):
    body = models.CharField(max_length=50, default=None)
    teacher_req = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='requests',
        related_query_name='request'  # <-- this line to avoid conflict
    )
    created_at = models.DateTimeField(default=datetime.now)

class Course(models.Model):
    name = models.CharField(max_length=50, default=None)
    student_courses = models.ManyToManyField(Student, default=None)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)