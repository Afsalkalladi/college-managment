from django.db import models
from django.utils import timezone
import os

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
    file = models.FileField(upload_to=teacher_resource_upload_path, blank=True, null=True)
    external_link = models.URLField(blank=True, null=True, help_text="For video links or external resources")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-uploaded_at']
        
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