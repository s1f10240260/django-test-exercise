from django.shortcuts import render, redirect
from django.http import Http404
from todo.models import Task


# Create your views here.
def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_at = request.POST.get('due_at') or None
        Task.objects.create(title=title, due_at=due_at)
        return redirect('index')

    order = request.GET.get('order')
    if order == 'due':
        tasks = Task.objects.order_by('due_at')
    elif order == 'post':
        tasks = Task.objects.order_by('posted_at')
    else:
        tasks = Task.objects.all()

    return render(request, 'todo/index.html', {'tasks': tasks})


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'todo/detail.html', {'task': task})
