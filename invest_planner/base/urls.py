from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, Taskupdate, DeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login'), name='account_logout'),
    
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', Taskupdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]