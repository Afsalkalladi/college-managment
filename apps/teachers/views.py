from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import TeacherResource, TeacherAssignment
from .forms import TeacherResourceForm
from apps.academics.models import AcademicYear

@login_required
def teacher_resource_list(request):
    """List all resources uploaded by the teacher"""
    if request.user.user_type != 'teacher':
        messages.error(request, "Access denied. Teachers only.")
        return redirect('home')
    
    teacher = request.user.teacher_profile
    resources = TeacherResource.objects.filter(teacher=teacher).select_related('subject')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )
    
    # Filter by subject
    subject_filter = request.GET.get('subject', '')
    if subject_filter:
        resources = resources.filter(subject__id=subject_filter)
    
    # Filter by resource type
    type_filter = request.GET.get('type', '')
    if type_filter:
        resources = resources.filter(resource_type=type_filter)
    
    # Pagination
    paginator = Paginator(resources, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get subjects for filter dropdown
    assigned_subjects = Subject.objects.filter(
        teacherassignment__teacher=teacher,
        teacherassignment__is_active=True
    ).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'assigned_subjects': assigned_subjects,
        'resource_types': TeacherResource.RESOURCE_TYPE_CHOICES,
        'selected_subject': subject_filter,
        'selected_type': type_filter,
    }
    
    return render(request, 'teachers/resource_list.html', context)

@login_required
def teacher_resource_create(request):
    """Create a new resource"""
    if request.user.user_type != 'teacher':
        messages.error(request, "Access denied. Teachers only.")
        return redirect('home')
    
    teacher = request.user.teacher_profile
    
    if request.method == 'POST':
        form = TeacherResourceForm(request.POST, request.FILES, teacher=teacher)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.teacher = teacher
            # Get current academic year
            resource.academic_year = AcademicYear.objects.filter(is_current=True).first()
            resource.save()
            messages.success(request, f"Resource '{resource.title}' uploaded successfully!")
            return redirect('teachers:resource_list')
    else:
        form = TeacherResourceForm(teacher=teacher)
    
    return render(request, 'teachers/resource_form.html', {'form': form, 'title': 'Upload Resource'})

@login_required
def teacher_resource_update(request, pk):
    """Update existing resource"""
    if request.user.user_type != 'teacher':
        messages.error(request, "Access denied. Teachers only.")
        return redirect('home')
    
    teacher = request.user.teacher_profile
    resource = get_object_or_404(TeacherResource, pk=pk, teacher=teacher)
    
    if request.method == 'POST':
        form = TeacherResourceForm(request.POST, request.FILES, instance=resource, teacher=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f"Resource '{resource.title}' updated successfully!")
            return redirect('teachers:resource_list')
    else:
        form = TeacherResourceForm(instance=resource, teacher=teacher)
    
    return render(request, 'teachers/resource_form.html', {'form': form, 'title': 'Update Resource'})

@login_required
def teacher_resource_delete(request, pk):
    """Delete resource"""
    if request.user.user_type != 'teacher':
        messages.error(request, "Access denied. Teachers only.")
        return redirect('home')
    
    teacher = request.user.teacher_profile
    resource = get_object_or_404(TeacherResource, pk=pk, teacher=teacher)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, f"Resource '{resource.title}' deleted successfully!")
        return redirect('teachers:resource_list')
    
    return render(request, 'teachers/resource_confirm_delete.html', {'resource': resource})