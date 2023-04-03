from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .Form import *
import traceback

def home(request):
    
    context = {
        

        }
    return render(request, 'pages/index.html', context)



def login_view(request):
    try:
        if request.method == 'POST':
            form = CustomAuthenticationForm(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, email=email, password=password, role__in=['student', 'teacher', 'admin'])
                
                if user is not None:
                    login(request, user)
                    
                   
                    if user.role == 'teacher':
                        return redirect('teacher_home')
                    elif user.role == 'student':
                        return redirect('student_home')
                    elif user.role == 'admin':
                        return redirect('admin_home')
                  
                else:
                    # Invalid login details
                    return render(request, 'login/login.html', {'form': form, 'error': 'Invalid login details' })

            else:
                # Form is not valid
                return render(request, 'login/login.html', {'form': form})

        else:
            # Display login form
            form = CustomAuthenticationForm()
            return render(request, 'login/login.html', {'form': form})

    except Exception as e:
        traceback.print_exc()

    


def logoutUser(request):
    logout(request)
    return redirect('login')


def add_teacher(request):

    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')

        teacher = CustomUser.objects.create(email=email, 
                                  first_name=first_name, 
                                  last_name=last_name, 
                                  is_staff=True, 
                                  role="teacher"
                                  )

        teacher.save()
        return render(request, 'pages/manageTeacher.html', {'teacher': teacher})
        
    else:
        return render(request, 'pages/manageTeacher.html')


def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')

        student = CustomUser.objects.create(email=email, 
                                  first_name=first_name, 
                                  last_name=last_name, 
                                  role="student"
                                  )
        student.save()
        return render(request, 'pages/manageStudent.html', {'student': student})
        
    else:
        return render(request, 'pages/manageStudent.html', {})