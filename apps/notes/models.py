from django.db import models

# Create your models here.
# models.py
def student_note_upload_path(instance, filename):
    """Creates hierarchical folder structure"""
    return f'student_notes/{instance.scheme.name}/sem_{instance.semester.number}/{instance.subject.code}/{filename}'

class StudentNote(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE)
    scheme = models.ForeignKey('academics.Scheme', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=student_note_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verification_status = models.CharField(max_length=20, default='pending')
    
class NoteVerification(models.Model):
    note = models.OneToOneField(StudentNote, on_delete=models.CASCADE)
    verified_by = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE)
    verification_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # 'approved', 'rejected', 'pending'
    feedback = models.TextField(blank=True)
    
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey('teachers.Assignment', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)