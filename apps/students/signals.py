# students/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentEnrollment, StudentSubjectEnrollment
from academics.models import Subject

@receiver(post_save, sender=StudentEnrollment)
def create_subject_enrollments(sender, instance, created, **kwargs):
    """Automatically enroll student in all subjects of their current semester"""
    if created or kwargs.get('update_fields') and 'current_semester' in kwargs.get('update_fields', []):
        # Get all subjects for the current semester
        subjects = Subject.objects.filter(
            semester=instance.current_semester,
            scheme=instance.scheme
        )
        
        # Create enrollment for each subject
        for subject in subjects:
            StudentSubjectEnrollment.objects.get_or_create(
                student=instance.student,
                subject=subject,
                semester=instance.current_semester,
                academic_year=instance.academic_year
            )