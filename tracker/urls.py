from django.urls import path
from .views import *

urlpatterns = [
    path('workers/', WorkersListView.as_view()),
    path('worker/new/', WorkersListView.as_view()),
    path('worker/<int:pk>/', WorkerDetailView.as_view()),
    path('worker/<int:pk>/edit/', WorkerDetailView.as_view()),
    path('worker/<int:pk>/delete/', WorkerDetailView.as_view()),
    path('tasks/', TasksListView.as_view()),
    path('task/new/', TasksListView.as_view()),
    path('task/<int:pk>/', TaskDetailView.as_view()),
    path('task/<int:pk>/edit/', TaskDetailView.as_view()),
    path('task/<int:pk>/delete/', TaskDetailView.as_view()),
    path('busy_workers/', BusyWorkersListAPIView.as_view()),
    path('necessary_tasks/', NecessaryTasksListAPIView.as_view()),
]
