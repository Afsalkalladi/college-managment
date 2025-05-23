# students/apps.py
from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.students'  # Use just 'students' if app is in root
    # name = 'apps.students'  # Use this if app is inside apps/ folder
    
    def ready(self):
        # Import signals when app is ready
        try:
            import students.signals
        except ImportError:
            pass  # Signals file doesn't exist yet