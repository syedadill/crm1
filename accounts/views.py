from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from .forms import TaskForm

def RegisterPage(request):
    context = {}
    return render(request, 'accounts/register.html', context)

def LoginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def home (request):
    project = Projects.objects.all()
    task = Tasks.objects.all()

    todo = task.filter(SelectStatus="ToDo").count()
    inprogress = task.filter(SelectStatus="In Progress").count()
    testing = task.filter(SelectStatus="Testing").count()
    bug = task.filter(SelectStatus="Bug").count()
    completed = task.filter(SelectStatus="Completed").count()
    context = {'project': project, 'task': task, 'todo': todo, 'inprogress': inprogress,'testing': testing, 'bug': bug, 'completed': completed, 'task': task }

    return render(request, 'accounts/dashboard.html', context)
def Task (request):
    tasklist = Tasks.objects.all()
    return render (request, 'accounts/task.html', {'tasklist':tasklist})
def Project (request, pk_test):
    projects = Projects.objects.get(id=pk_test)
    task = projects.tasks_set.all()
    task_count = task.filter(SelectStatus='ToDo').count()

    context = {'project': projects, 'task': task, 'task_count': task_count}

    return render (request, 'accounts/projects.html', context)

def CreateTask(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form': form}
    return render (request, 'accounts/form.html', context)

def UpdateTask(request, pk):
    task = Tasks.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render (request, 'accounts/form.html', context)
    
def DeleteTask(request, pk):
    task = Tasks.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    context = {'task': task}
    return render (request, 'accounts/delete.html', context)
# Create your views here.

def Task_Detail(request, pk):
    task = Tasks.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form, 'task': task}
    return render (request, 'accounts/status.html', context)