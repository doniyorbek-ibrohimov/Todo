from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *


class IndexView(View):
    def get(self, request):
        statuses = Task.STATUS_CHOICES
        tasks = Task.objects.order_by('-status', '-created_at')
        context = {
            'statuses': statuses,
            'tasks':tasks
        }
        return render(request, 'index.html', context)

    def post(self, request):
        Task.objects.create(
            title=request.POST.get('title'),
            deadline=None if request.POST.get('deadline') == "" else request.POST.get('deadline'),
            status=request.POST.get('status'),
            details=request.POST.get('details'),
        )
        return redirect('index')


def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('index')


class TaskEditView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        context = {
            'task': task,
            'statuses': Task.STATUS_CHOICES,
        }
        return render(request, 'edit.html', context)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.title = request.POST.get('title')
        task.details = request.POST.get('details')
        task.status = request.POST.get('status')
        task.save()
        return redirect('index')
