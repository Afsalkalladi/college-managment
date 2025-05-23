# teachers/models.py
from django.db import models
from django.utils import timezone
import os
from .utils import validate_file_extension, validate_file_size

def teacher_resource_upload_path(instance, filename):
    # Create path: teacher_resources/subject_code/year/filename
    year = timezone.now().year
    return f'teacher_resources/{instance.subject.code}/{year}/{filename}'

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['teacher', 'subject', 'academic_year']
        
    def __str__(self):
        return f"{self.teacher} - {self.subject}"

class TeacherResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('lecture', 'Lecture Notes'),
        ('presentation', 'Presentation'),
        ('assignment', 'Assignment'),
        ('reference', 'Reference Material'),
        ('video', 'Video Link'),
        ('other', 'Other'),
    ]
    
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES, default='lecture')
    file = models.FileField(
        upload_to=teacher_resource_upload_path, 
        blank=True, 
        null=True,
        validators=[validate_file_extension, validate_file_size],
        help_text='Allowed file types: PDF, DOC, DOCX, PPT, PPTX, TXT, ZIP, RAR. Max size: 10MB'
    )
    external_link = models.URLField(blank=True, null=True, help_text="For video links or external resources")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['subject', 'is_active']),
            models.Index(fields=['teacher', 'uploaded_at']),
        ]
        
    def __str__(self):
        return f"{self.title} - {self.subject.code}"
    
    def get_file_size(self):
        if self.file:
            return f"{self.file.size / 1024 / 1024:.2f} MB"
        return "N/A"
    
    def get_file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1][1:].upper()
        return "N/A"
    
    def clean(self):
        """Additional validation to ensure either file or external link is provided"""
        from django.core.exceptions import ValidationError
        
        if not self.file and not self.external_link:
            raise ValidationError("Either a file or an external link must be provided.")
        
        if self.file and self.external_link:
            raise ValidationError("Please provide either a file or an external link, not both.")
    
    def save(self, *args, **kwargs):
        # Run full clean validation before saving
        self.full_clean()
        super().save(*args, **kwargs)

class Assignment(models.Model):
    """Model for assignments given by teachers"""
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(
        upload_to='assignments/', 
        blank=True,
        validators=[validate_file_extension, validate_file_size],
        help_text='Optional: Attach assignment document. Max size: 10MB'
    )
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_marks = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subject', 'due_date']),
            models.Index(fields=['teacher', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.subject.code}"
    
    @property
    def is_past_due(self):
        return timezone.now() > self.due_dateclear
    
    def get_submission_count(self):
        return self.assignmentsubmission_set.count()
    
    def get_pending_submissions(self):
        from students.models import StudentSubjectEnrollment
        enrolled_students = StudentSubjectEnrollment.objects.filter(
            subject=self.subject,
            academic_year=self.academic_year
        ).count()
        return enrolled_students - self.get_submission_count()