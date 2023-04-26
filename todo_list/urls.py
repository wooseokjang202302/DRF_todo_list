from django.urls import path
from todo_list import views


urlpatterns = [
    path('', views.ToDoListView.as_view(), name='todo_list_view'),
    path('create/', views.ToDoListView.as_view(), name='create_todo_list_view'),
    path('<int:todo_list_id>/', views.ToDoListDetailView.as_view(),
         name='todo_list_detail_view'),
    path('<int:todo_list_id>/update/', views.ToDoListDetailView.as_view(),
         name='update_todo_list_detail_view'),
    path('<int:todo_list_id>/delete/', views.ToDoListDetailView.as_view(),
         name='delete_todo_list_detail_view'),
]
