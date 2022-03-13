
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Task
from .forms import TodoForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
# Create your views here.


# class TaskListView(ListView):
#     model = Task
#     template_name = 'todo/index.html'
#     context_object_name = 'task_list'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todo/detail.html'
    context_object_name = 'task'


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'todo/update.html'
    context_object_name = 'task'
    fields = ['name', 'priority', 'date']

    def get_success_url(self):
        return reverse_lazy('todo:todohome')


# class TaskDeleteView(DeleteView):
#     model = Task
#     template_name = 'todo/delete_task.html'
#     success_url = reverse_lazy('todo:cbvindex')


def index(request):
    task_list = Task.objects.all()
    if request.method == "POST":
        name = request.POST.get('name',)
        priority = request.POST.get('priority',)
        date = request.POST.get('date',)
        task = Task(name=name, priority=priority, date=date)

        task.save()
        return redirect('todo:todohome')
    context = {'task_list': task_list}
    return render(request, 'todo/index.html', context)


def delete_task(request, id):
    task = Task.objects.get(id=id)
    context = {
        "task": task
    }
    if request.method == "POST":
        task.delete()
        return redirect('todo:todohome')
    return render(request, 'todo/delete_task.html', context)


def update(request, id):
    task = Task.objects.get(id=id)
    form = TodoForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        return redirect('todo:todohome')
    context = {
        "task": task,
        "form": form
    }
    return render(request, 'todo/edit.html', context)
