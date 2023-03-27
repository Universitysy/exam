from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group


class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Students must have an email address')
        student = self.model(email=self.normalize_email(email), **kwargs)
        student.set_password(password)
        student.save()
        return student
    
class Student(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name= 'student_group',
        blank=True,
        help_text= 
            'The groups this user belongs to. A student will get all permissions '
            'granted to each of their groups.'
        ,
        related_name='students'
        )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="student_user_permissions",
        verbose_name='student permissions',
        help_text='Specific permissions for this user.',
    )
    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class TeacherManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Teachers must have an email address')
        teacher = self.model(email=self.normalize_email(email), **kwargs)
        teacher.set_password(password)
        teacher.save()
        return teacher

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)



class Teacher(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name= 'teacher_group',
        blank=True,
        help_text= 
            'The groups this user belongs to. A teacher will get all permissions '
            'granted to each of their groups.'
        ,
        related_name='teachers'
        )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="teacher_user_permissions",
        verbose_name='teacher permissions',
        help_text='Specific permissions for this teacher.',
    )
    objects = TeacherManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name




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