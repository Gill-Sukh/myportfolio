from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='todohome'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    # path('update/<int:id>/', views.update, name='update'),
    # path('cbvindex/', views.TaskListView.as_view(), name=''),
    path('cbvdetail/<int:pk>/', views.TaskDetailView.as_view(), name='cbvdetail'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='update'),
    #     path('cbvdelete/<int:pk>/', views.TaskDeleteView.as_view(), name='cbvdelete'),
]
