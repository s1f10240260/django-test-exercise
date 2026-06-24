from django.urls import path
from todo.views import CreateTaskView

app_name = 'todo'

urlpatterns = [
    path('create/', CreateTaskView.as_view(), name='create'),
]
