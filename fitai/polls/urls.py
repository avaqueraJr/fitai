from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('workout_routine/', views.workout_routine, name='workout_routine'),
    path('polls/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('polls/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('polls/register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('fitness_data/', views.fitness_data, name='fitness_data'),
]
