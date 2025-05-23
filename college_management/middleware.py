# college_management/middleware.py
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class UserTypeMiddleware:
    """Middleware to ensure users can only access their designated areas"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'user_type'):
            path = request.path
            user_type = request.user.user_type
            
            # Define restricted paths
            teacher_paths = ['/teacher/', '/teachers/']
            student_paths = ['/student/', '/students/']
            admin_paths = ['/admin/']
            
            # Check access permissions
            if any(path.startswith(p) for p in teacher_paths) and user_type != 'teacher':
                messages.error(request, "Access denied. This area is for teachers only.")
                return redirect('accounts:dashboard')
            
            elif any(path.startswith(p) for p in student_paths) and user_type != 'student':
                messages.error(request, "Access denied. This area is for students only.")
                return redirect('accounts:dashboard')
            
            elif any(path.startswith(p) for p in admin_paths) and user_type != 'admin' and not request.user.is_superuser:
                messages.error(request, "Access denied. Admin access required.")
                return redirect('accounts:dashboard')
        
        response = self.get_response(request)
        return response