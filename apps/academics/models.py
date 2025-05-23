from django.db import models

class Scheme(models.Model):
    name = models.CharField(max_length=50)
    start_year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Scheme {self.name}"

class AcademicYear(models.Model):
    year = models.CharField(max_length=9)  # e.g., "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.year

class Semester(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ['scheme', 'number']
        
    def __str__(self):
        return f"{self.name} - {self.scheme.name}"

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    credits = models.IntegerField()
    is_lab = models.BooleanField(default=False)
    is_elective = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.code} - {self.name}"