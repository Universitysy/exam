from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Permission
from django.db import models
from datetime import datetime


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ADMIN')

    objects = UserManager()


class StudentManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)
    def get_queryset(self):
        return super().get_queryset().filter(role='STUDENT')

class Student(User):
    objects = StudentManager()
    

    class Meta:
        proxy = True


class TeacherManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)
    def get_queryset(self):
        return super().get_queryset().filter(role='TEACHER')

class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True


class AdminManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)
    def get_queryset(self):
        return super().get_queryset().filter(role='ADMIN')

class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True










class Request_t(models.Model):
    body = models.CharField(max_length=50, default=None)
    status = models.BooleanField(default=False)
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


class Time_A(models.Model):
      time_choices = [
        ('8:00 --> 9:00 AM', '8:00 --> 9:00 AM'),
        ('9:00 --> 10:00 AM', '8:00 --> 10:00 AM'),
        ('10:00 --> 11:00 AM', '8:00 --> 11:00 AM'),
        ('11:00 --> 12:00 PM', '8:00 --> 12:00 PM'),
        ('12:00 --> 1:00 PM', '8:00 --> 1:00 PM'),
        ('1:00 --> 2:00 PM', '8:00 --> 2:00 PM'),
        ('2:00 --> 3:00 PM', '8:00 --> 3:00 PM'),
        ('3:00 --> 4:00 PM', '8:00 --> 4:00 PM'),
        # Add more choices as needed
    ]

      time = models.TimeField(choices=time_choices)

      date = models.DateField()
