from errno import EOWNERDEAD

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from django.contrib.auth import authenticate, login, logout


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            statuses = Task.STATUS_CHOICES
            tasks = Task.objects.filter(owner=request.user).order_by('-status', '-created_at')
            context = {
                'statuses': statuses,
                'tasks': tasks
            }
            return render(request, 'index.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            Task.objects.create(
                title=request.POST.get('title'),
                deadline=None if request.POST.get('deadline') == "" else request.POST.get('deadline'),
                status=request.POST.get('status'),
                details=request.POST.get('details'),
                owner=request.user
            )
            return redirect('index')
        return redirect('login')


def task_delete_view(request, pk):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk, owner=request.user)
        task.delete()
        return redirect('index')
    return redirect('login')


class TaskEditView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, pk=pk, owner=request.user)
            context = {
                'task': task,
                'statuses': Task.STATUS_CHOICES,
            }
            return render(request, 'edit.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, pk=pk, owner=request.user)
            task.title = request.POST.get('title')
            task.details = request.POST.get('details')
            task.status = request.POST.get('status')
            task.save()
            return redirect('index')
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('password1') != request.POST.get('password2') or request.POST.get(
                'username') in User.objects.values_list('username', flat=True):
            return redirect('register')
        User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password1'),
        )
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        print(user)
        if user is not None:
            login(request, user)
            return redirect('index')
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')
