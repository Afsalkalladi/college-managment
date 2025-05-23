from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentEnrollment(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    scheme = models.ForeignKey('academics.Scheme', on_delete=models.CASCADE)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    current_semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'academic_year']
        
    def __str__(self):
        return f"{self.student} - {self.academic_year}"

class StudentSubjectEnrollment(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'academic_year']
        
    def __str__(self):
        return f"{self.student} - {self.subject}"