from django.urls import path
from .import views 


urlpatterns = [
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.LoginPage, name='login'),

    path('', views.home , name="home"),
    path('task/', views.Task, name="task"),
    path('projects/<str:pk_test>/', views.Project, name="projects"),
    
    path('create_task', views.CreateTask, name='create_task'),
    path('update_task/<str:pk>/', views.UpdateTask, name='update_task'),
    path('delete_task/<str:pk>/', views.DeleteTask, name='delete_task'),
    path('task-details/<int:pk>/', views.Task_Detail, name='get_task_details'),
]

