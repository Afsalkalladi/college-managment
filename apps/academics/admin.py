from django.contrib import admin
from .models import Scheme, AcademicYear, Semester, Subject

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['year']  # Required for autocomplete
    ordering = ['-start_date']

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_year', 'is_active']
    list_filter = ['is_active', 'start_year']
    search_fields = ['name']  # Required for autocomplete
    ordering = ['-start_year']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'scheme', 'number']
    list_filter = ['scheme', 'number']
    search_fields = ['name', 'scheme__name']  # Required for autocomplete
    ordering = ['scheme', 'number']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'scheme', 'semester', 'credits', 'is_lab', 'is_elective']
    list_filter = ['scheme', 'semester', 'is_lab', 'is_elective']
    search_fields = ['code', 'name', 'scheme__name']  # Required for autocomplete
    ordering = ['scheme', 'semester', 'code']
    autocomplete_fields = ['scheme', 'semester']
