from django.urls import path
from todo.views import index, detail

urlpatterns = [
    path('', index, name='index'),
    path('<int:task_id>/', detail, name='detail'),
]
