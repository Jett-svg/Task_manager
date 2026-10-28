from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/toggle/', views.task_toggle, name='task_toggle'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('stats/', views.task_stats, name='task_stats'),
]