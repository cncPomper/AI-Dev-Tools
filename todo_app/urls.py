from django.urls import path
from . import views

app_name = 'todo_app' # Namespace for URLs

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('<int:pk>/toggle_resolved/', views.todo_toggle_resolved, name='todo_toggle_resolved'),
]