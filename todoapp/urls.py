from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('completed/', views.completed_view, name='completed'),

    path('delete/<int:task_id>/', views.task_delete_view, name='task_delete'),
    path('complete/<int:task_id>/', views.task_complete_view, name='task_complete'),
    path('dump/<int:task_id>/', views.task_dump_view, name='task_dump'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]