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




class Room(models.Model):
    name = models.CharField( max_length=20, default=None)
    max_capacity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)




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



class Teacher_Availability(models.Model):
    class Meta:
        verbose_name = 'Teacher_Availability'
        verbose_name_plural = 'Teacher_Availabilities'

      
    teacher_av = models.ForeignKey(Teacher, on_delete= models.CASCADE)
    time_start = models.TimeField(default=None)
    time_end = models.TimeField(default=None)

    date = models.DateField(default=None)


class Course(models.Model):
    name = models.CharField(max_length=50, default=None)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)



class Exam(models.Model):

    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    date = models.DateField()
    assigned_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    course_exam = models.ForeignKey(Course, on_delete=models.CASCADE)



class Selected_exam(models.Model):
    t_a = models.ForeignKey(Teacher_Availability,related_name='ta',
                            related_query_name='ta', on_delete= models.CASCADE)
    e_x = models.ForeignKey(Exam, related_name='ex',
                            related_query_name='ex' ,on_delete= models.CASCADE)
   
    class Meta:
        unique_together = ('t_a', 'e_x')

   

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




class Exam_Swap_Request(models.Model):
    body = models.CharField(max_length=50, default=None)
    status = models.BooleanField(default=False)
    requesting_professor = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='requested_swaps',
        related_query_name='requested_swaps'  # <-- this line to avoid conflict
    )
    responding_professor = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='responded_swaps',
        related_query_name='responded_swaps'  # <-- this line to avoid conflict
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)




class Exam_Registration(models.Model):
    tecaher_exam_registration = models.ForeignKey(Teacher, on_delete=models.CASCADE , related_name='teacher_registrations')
    registration_date_time = models.DateTimeField(default=datetime.now)
    registered_student = models.ForeignKey(Student, on_delete= models.CASCADE)
    associated_exam =  models.ForeignKey(Exam, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10, default='SA1')










