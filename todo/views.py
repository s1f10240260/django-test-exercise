from django.shortcuts import render
from django.views.generic.edit import CreateView
from todo.models import Task

# Create your views here.
class CreateTaskView(CreateView):
    model = Task
    fields = ['title', 'due_at']
    template_name = 'todo/task_form.html'
    success_url = '/todo/create/'
