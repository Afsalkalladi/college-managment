from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentEnrollment, StudentSubjectEnrollment

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'scheme', 'academic_year', 'current_semester', 'is_active']
    list_filter = ['is_active', 'academic_year', 'scheme', 'current_semester']
    search_fields = ['student__user__username', 'student__roll_number']
    autocomplete_fields = ['student', 'scheme', 'academic_year', 'current_semester']

@admin.register(StudentSubjectEnrollment)
class StudentSubjectEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'semester', 'academic_year', 'enrolled_date']
    list_filter = ['academic_year', 'semester', 'enrolled_date']
    search_fields = ['student__user__username', 'student__roll_number', 'subject__name', 'subject__code']
    autocomplete_fields = ['student', 'subject', 'semester', 'academic_year']
    readonly_fields = ['enrolled_date']