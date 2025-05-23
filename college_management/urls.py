# college_management/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls', namespace='accounts')),
    path('academics/', include('apps.academics.urls', namespace='academics')),
    path('student/', include('apps.students.urls', namespace='students')),
    path('teacher/', include('apps.teachers.urls', namespace='teachers')),
    path('notes/', include('apps.notes.urls', namespace='notes')),
    path('library/', include('apps.library.urls', namespace='library')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)