from django.shortcuts import render

# Create your views here.
# apps/library/views.py
def library_browse(request, scheme=None, semester=None, subject=None):
    context = {}
    
    if not scheme:
        # Show all schemes
        context['schemes'] = Scheme.objects.filter(is_active=True)
    elif not semester:
        # Show semesters for selected scheme
        context['scheme'] = get_object_or_404(Scheme, name=scheme)
        context['semesters'] = Semester.objects.filter(scheme=context['scheme'])
    elif not subject:
        # Show subjects for selected semester
        context['scheme'] = get_object_or_404(Scheme, name=scheme)
        context['semester'] = get_object_or_404(Semester, scheme=context['scheme'], number=semester)
        context['subjects'] = Subject.objects.filter(
            scheme=context['scheme'],
            semester=context['semester']
        )
    else:
        # Show notes for selected subject
        context['notes'] = LibraryNote.objects.filter(
            student_note__scheme__name=scheme,
            student_note__semester__number=semester,
            student_note__subject__code=subject
        ).select_related('student_note')
    
    return render(request, 'library/browse.html', context)