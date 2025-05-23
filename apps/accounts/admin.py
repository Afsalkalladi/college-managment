from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import TeacherProfile, StudentProfile

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    """Custom admin for User model with user_type field"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    # Add user_type to the fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'is_verified')
        }),
    )
    
    # Add user_type to add_fieldsets for creating new users
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'email', 'first_name', 'last_name')
        }),
    )

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    # Remove 'department' and 'created_at' if they don't exist in your model
    list_display = ['user', 'employee_id', 'qualification', 'specialization']
    list_filter = ['qualification']  # Remove 'department' and 'created_at'
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'employee_id']
    autocomplete_fields = ['user']
    # Remove readonly_fields if created_at and updated_at don't exist
    # readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Details', {
            'fields': ('employee_id', 'qualification', 'specialization', 'experience_years')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
        # Remove timestamp fieldset if fields don't exist
        # ('Timestamps', {
        #     'fields': ('created_at', 'updated_at'),
        #     'classes': ('collapse',)
        # }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    # Remove 'department' and 'created_at' if they don't exist in your model
    list_display = ['user', 'roll_number', 'admission_year', 'current_semester']
    list_filter = ['admission_year', 'current_semester']  # Remove 'department' and 'created_at'
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'roll_number']
    autocomplete_fields = ['user']
    # Remove readonly_fields if created_at and updated_at don't exist
    # readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Details', {
            'fields': ('roll_number', 'admission_year', 'current_semester')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'phone_number', 'address')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email'),
            'classes': ('collapse',)
        }),
        # Remove timestamp fieldset if fields don't exist
        # ('Timestamps', {
        #     'fields': ('created_at', 'updated_at'),
        #     'classes': ('collapse',)
        # }),
    )

# Register the custom user admin
# Remove the unregister line since User model is not registered by default in this context
admin.site.register(User, CustomUserAdmin)