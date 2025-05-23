from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('resources/', views.teacher_resource_list, name='resource_list'),
    path('resources/create/', views.teacher_resource_create, name='resource_create'),
    path('resources/<int:pk>/update/', views.teacher_resource_update, name='resource_update'),
    path('resources/<int:pk>/delete/', views.teacher_resource_delete, name='resource_delete'),
]