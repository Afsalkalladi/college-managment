from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('resources/', views.student_resources, name='resource_list'),
    path('resources/<int:pk>/download/', views.student_resource_download, name='resource_download'),
]