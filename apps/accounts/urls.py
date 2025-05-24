from django.urls import path
from . import views

app_name = 'apps.accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('register/teacher/', views.teacher_register, name='teacher_register'),
    path('register/student/', views.student_register, name='student_register'),
]