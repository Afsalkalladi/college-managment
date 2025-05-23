from django.contrib import admin
from .models import TeacherAssignment, TeacherResource

@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'academic_year', 'is_active', 'assigned_date']
    list_filter = ['is_active', 'academic_year', 'assigned_date']
    search_fields = ['teacher__user__username', 'subject__name', 'subject__code']
    autocomplete_fields = ['teacher', 'subject', 'academic_year']

@admin.register(TeacherResource)
class TeacherResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'subject', 'resource_type', 'uploaded_at', 'is_active']
    list_filter = ['resource_type', 'is_active', 'uploaded_at', 'academic_year']
    search_fields = ['title', 'description', 'teacher__user__username', 'subject__name']
    readonly_fields = ['uploaded_at', 'updated_at']
    autocomplete_fields = ['teacher', 'subject', 'academic_year']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('teacher', 'subject', 'academic_year', 'title', 'description')
        }),
        ('Resource Details', {
            'fields': ('resource_type', 'file', 'external_link')
        }),
        ('Status', {
            'fields': ('is_active', 'uploaded_at', 'updated_at')
        }),
    )