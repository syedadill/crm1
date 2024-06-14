from django.urls import path
from django.contrib.auth import views as auth_views
from .import views 


urlpatterns = [
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),

    path('', views.home , name="home"),
    path('user/', views.userPage, name="user-page"),
    path('task/', views.Task, name="task"),
    path('projects/<str:pk_test>/', views.Project, name="projects"),
    path('employee/<str:pk_test>/', views.Customer, name="employee"),

    
    path('create_project', views.CreateProject, name='create_project'),
    path('update_project/<str:pk>/', views.UpdateProject, name='update_project'),
    path('create_task/<int:project_id>/', views.CreateTask, name='create_task'),
    path('update_task/<str:pk>/', views.UpdateTask, name='update_task'),
    path('delete_task/<str:pk>/', views.DeleteTask, name='delete_task'),
    path('task-details/<int:pk>/', views.Task_Detail, name='get_task_details'),
    path('account', views.ProfileSettings, name='account'),
    path('update_status/<str:pk>/', views.UpdateTaskUser, name='update_status'),
    path('comments/<str:pk>/', views.Comments, name='comments'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name = "password_reset_complete"),


    ]

