from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q
from teachers.models import TeacherResource
from .models import StudentEnrollment, StudentSubjectEnrollment
from academics.models import AcademicYear
import mimetypes
import os

@login_required
def student_resources(request):
    """View resources for enrolled subjects only"""
    if request.user.user_type != 'student':
        messages.error(request, "Access denied. Students only.")
        return redirect('home')
    
    student = request.user.student_profile
    
    # Get current enrollment
    current_enrollment = StudentEnrollment.objects.filter(
        student=student,
        is_active=True
    ).first()
    
    if not current_enrollment:
        messages.warning(request, "You are not currently enrolled in any semester.")
        return render(request, 'students/no_enrollment.html')
    
    # Get enrolled subjects for current semester
    enrolled_subjects = StudentSubjectEnrollment.objects.filter(
        student=student,
        semester=current_enrollment.current_semester,
        academic_year=current_enrollment.academic_year
    ).values_list('subject', flat=True)
    
    # Get resources for enrolled subjects only
    resources = TeacherResource.objects.filter(
        subject__in=enrolled_subjects,
        is_active=True,
        academic_year=current_enrollment.academic_year
    ).select_related('subject', 'teacher__user')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__name__icontains=search_query) |
            Q(teacher__user__first_name__icontains=search_query) |
            Q(teacher__user__last_name__icontains=search_query)
        )
    
    # Filter by subject
    subject_filter = request.GET.get('subject', '')
    if subject_filter:
        resources = resources.filter(subject__id=subject_filter)
    
    # Filter by resource type
    type_filter = request.GET.get('type', '')
    if type_filter:
        resources = resources.filter(resource_type=type_filter)
    
    # Group resources by subject
    resources_by_subject = {}
    for resource in resources:
        subject_name = resource.subject.name
        if subject_name not in resources_by_subject:
            resources_by_subject[subject_name] = []
        resources_by_subject[subject_name].append(resource)
    
    # Get subjects for filter dropdown
    enrolled_subject_objects = Subject.objects.filter(id__in=enrolled_subjects)
    
    context = {
        'resources_by_subject': resources_by_subject,
        'search_query': search_query,
        'enrolled_subjects': enrolled_subject_objects,
        'resource_types': TeacherResource.RESOURCE_TYPE_CHOICES,
        'selected_subject': subject_filter,
        'selected_type': type_filter,
        'current_semester': current_enrollment.current_semester,
    }
    
    return render(request, 'students/resource_list.html', context)

@login_required
def student_resource_download(request, pk):
    """Download resource file"""
    if request.user.user_type != 'student':
        messages.error(request, "Access denied. Students only.")
        return redirect('home')
    
    student = request.user.student_profile
    resource = get_object_or_404(TeacherResource, pk=pk, is_active=True)
    
    # Check if student is enrolled in this subject
    current_enrollment = StudentEnrollment.objects.filter(
        student=student,
        is_active=True
    ).first()
    
    is_enrolled = StudentSubjectEnrollment.objects.filter(
        student=student,
        subject=resource.subject,
        academic_year=current_enrollment.academic_year
    ).exists()
    
    if not is_enrolled:
        raise Http404("You don't have access to this resource.")
    
    if resource.file:
        file_path = resource.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                mime_type, _ = mimetypes.guess_type(file_path)
                response = HttpResponse(fh.read(), content_type=mime_type)
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
                return response
    
    raise Http404("File not found.")