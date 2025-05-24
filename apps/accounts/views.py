from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomLoginForm, TeacherRegistrationForm, StudentRegistrationForm
from .models import TeacherProfile, StudentProfile

def login_view(request):
    """Common login view for all users"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_verified or user.is_superuser:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    
                    # Redirect based on user type
                    if user.user_type == 'teacher':
                        return redirect('teachers:resource_list')
                    elif user.user_type == 'student':
                        return redirect('students:resource_list')
                    elif user.is_superuser:
                        return redirect('admin:index')
                    else:
                        return redirect('accounts:dashboard')
                else:
                    messages.error(request, 'Your account is pending approval. Please contact the administrator.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def teacher_register(request):
    """Teacher registration view"""
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                'Registration successful! Your account is pending approval. You will be notified once approved.'
            )
            return redirect('accounts:login')
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'accounts/teacher_register.html', {'form': form})

def student_register(request):
    """Student registration view"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                'Registration successful! Your account is pending approval. You will be notified once approved.'
            )
            return redirect('accounts:login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/student_register.html', {'form': form})

@login_required
def dashboard(request):
    """Common dashboard that redirects based on user type"""
    user = request.user
    
    if user.user_type == 'teacher':
        return redirect('teachers:resource_list')
    elif user.user_type == 'student':
        return redirect('students:resource_list')
    elif user.is_superuser:
        return redirect('admin:index')
    else:
        return render(request, 'accounts/dashboard.html')

@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """View user profile"""
    context = {'user': request.user}
    
    if request.user.user_type == 'teacher':
        context['teacher_profile'] = request.user.teacher_profile
        template = 'accounts/teacher_profile.html'
    elif request.user.user_type == 'student':
        context['student_profile'] = request.user.student_profile
        template = 'accounts/student_profile.html'
    else:
        template = 'accounts/profile.html'
    
    return render(request, template, context)

def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'accounts/home.html')