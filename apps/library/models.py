from django.db import models

# models.py
class LibraryCategory(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    
class LibraryNote(models.Model):
    """Only approved notes appear in library"""
    student_note = models.OneToOneField('notes.StudentNote', on_delete=models.CASCADE)
    category = models.ForeignKey(LibraryCategory, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-added_date']