from django.shortcuts import render

# Create your views here.
# apps/students/views.py
@login_required
def student_resources(request):
    student = request.user.studentprofile
    enrollment = StudentEnrollment.objects.get(student=student, is_active=True)
    
    # Get current subjects
    current_subjects = StudentSubjectEnrollment.objects.filter(
        student=student,
        semester=enrollment.current_semester
    ).values_list('subject', flat=True)
    
    # Get teacher resources for enrolled subjects only
    resources = TeacherResource.objects.filter(
        subject__in=current_subjects,
        is_active=True
    ).select_related('teacher', 'subject')
    
    return render(request, 'students/resources.html', {'resources': resources})