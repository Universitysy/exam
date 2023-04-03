from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_student(self, email, password=None, **extra_fields):
        return self.create_user(email, password=password, role='student', **extra_fields)

    def create_teacher(self, email, password=None, **extra_fields):
        return self.create_user(email, password=password, role='teacher', **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=(('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')), default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_student(self):
        return self.role == 'student'
        
    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_admin(self):
        return self.role == 'admin'




class Request_t(models.Model):
    body = models.CharField(max_length=50, default=None)
    teacher_req = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='requests',
        related_query_name='request'  # <-- this line to avoid conflict
    )
    created_at = models.DateTimeField(default=datetime.now)

class Course(models.Model):
    name = models.CharField(max_length=50, default=None)
    student_courses = models.ManyToManyField(CustomUser, default=None)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)