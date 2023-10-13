from django.urls import path
from .import  views
from django.views.generic import TemplateView

app_name = 'usrs'

urlpatterns=[
     path('register/',TemplateView.as_view(template_name='registration/register.html'), name='register'),
     path('student_register/',views.StudentRegister.as_view(), name='student_register'),
     path('teacher_register/',views.TeacherRegister.as_view(), name='teacher_register'),
     path('index/', TemplateView.as_view(template_name='index.html'), name='home'),
     path('student/', views.StudentHome.as_view(), name='student'),
     path('teacher/', views.TeacherHome.as_view(), name='teacher'),
     path('login/',views.LoginView.as_view(), name='login'),
     path('logout/',views.LogoutView.as_view(), name='logout'),
     path('profile/',views.UserProfile.as_view(), name='profile'),
     path('error',TemplateView.as_view(template_name='404.html'), name='error')
]