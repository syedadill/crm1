from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from .forms import TaskForm, CreateUserForm,ProjectForm, EmployeeForm, CHangeStatus, CommentForm, ArticleForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.mail import send_mail

@unauthenticated_user
def RegisterPage(request):
        
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

               
               
                
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


@unauthenticated_user
def LoginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect!')
    context = {}
    return render(request, 'accounts/login.html', context)

def LogoutPage(request):
    logout(request)

    return redirect('login')

@login_required(login_url = 'login')
@admin_only
def home (request):
    project = Projects.objects.all()
    task = Tasks.objects.all()
    employee = Customers.objects.all()

    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    



    todo = task.filter(SelectStatus="ToDo").count()
    inprogress = task.filter(SelectStatus="In Progress").count()
    testing = task.filter(SelectStatus="Testing").count()
    bug = task.filter(SelectStatus="Bug").count()
    completed = task.filter(SelectStatus="Completed").count()
    context = {'project': project, 'task': task, 'employee': employee, 'todo': todo, 'inprogress': inprogress,'testing': testing, 'bug': bug, 'completed': completed, 'task': task, 'form':form }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['employee'])
def userPage(request):

    project = request.user.customers.projects_set.all()
    task = request.user.customers.tasks_set.all()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-page')
    
    
    notifications = Notification.objects.filter(user=request.user, is_read=False)


    todo = task.filter(SelectStatus="ToDo").count()
    inprogress = task.filter(SelectStatus="In Progress").count()
    testing = task.filter(SelectStatus="Testing").count()
    bug = task.filter(SelectStatus="Bug").count()
    completed = task.filter(SelectStatus="Completed").count()
        
    context = {'project':project,'notifications': notifications, 'form': form, 'task': task, 'todo': todo, 'inprogress': inprogress,'testing': testing, 'bug': bug, 'completed': completed, 'task': task  }
    return render (request, 'accounts/user.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['employee'])
def ProfileSettings(request):
    customer = request.user.customers
    form = EmployeeForm(instance=customer)

    if request.method=='POST':
        form = EmployeeForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render (request, 'accounts/account_settings.html', context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def Task (request):
    tasklist = Tasks.objects.all()
    return render (request, 'accounts/task.html', {'tasklist':tasklist})



@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin','employee'])
def Comments (request):
    comments = Comment.objects.all()
    return render (request, 'accounts/comment.html', {'comments':comments})


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin','employee'])
def Project (request, pk_test):
    projects = Projects.objects.get(id=pk_test)
    project = request.user.customers.projects_set.all()
    employee = Projects.objects.all()
    task = projects.tasks_set.all()
    task_count =  task.filter(SelectStatus='ToDo').count()


    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form,'employee':employee,'projects': projects,'project': project, 'task': task, 'task_count': task_count}

    return render (request, 'accounts/projects.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def Customer (request, pk_test):
    employee = Customers.objects.get(id=pk_test)
    task = employee.tasks_set.all()
    task_count =  task.filter(SelectStatus='ToDo').count()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form, employee: employee, 'task': task, 'task_count': task_count}

    return render (request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def CreateTask(request, project_id):
    project = Projects.objects.get(id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            message = f'Admin has assigned you a task: {task.TaskName}'
            Notification.objects.create(user=task.employe.user, message=message)
            
            if task.employe and task.employe.email:  # Make sure the employee has an email
                send_mail(
                    subject='New Task Assigned',
                    message=f'Dear {task.employe},\n\nYou have been assigned a new task: {task.TaskName}.\n\nDue Date: {task.DueDate}\n\nPlease check your task management system for more details.',
                    from_email='adilfazal03@gmail.com',
                    recipient_list=[task.employe.email],
                )
            return redirect('/')
    else:
        form = TaskForm(project=project)
    context = {'form': form, 'project':project}
    return render(request, 'accounts/form.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def CreateProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form': form}
    return render (request, 'accounts/projectform.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def UpdateProject(request, pk):
    project = Projects.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form': form}
    return render (request, 'accounts/projectform.html', context)







@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin','employee'])
def UpdateTask(request, pk):
    task = Tasks.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,request.FILES, instance=task)
        if form.is_valid():
            task=form.save()
            message = f'Admin has assigned you a task: {task.TaskName}'
            Notification.objects.create(user=task.employe.user, message=message)

            if task.employe and task.employe.email:  # Make sure the employee has an email
                send_mail(
                    subject='Task Updated',
                    message=f'Dear {task.employe},\n\n: {task.TaskName} has been updated and assigned to you.\n\nDue Date: {task.DueDate}\n\nPlease check your task management system for more details.',
                    from_email='adilfazal03@gmail.com',
                    recipient_list=[task.employe.email],
                )
            return redirect('/')
        
    context = {'form': form}
    return render (request, 'accounts/form.html', context)
    

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin','employee'])
def UpdateTaskUser(request, pk):
    task = Tasks.objects.get(id=pk)
    form = CHangeStatus(instance=task)
    if request.method == 'POST':
        form = CHangeStatus(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
      
        if task.employe and task.employe.email:  # Make sure the employee has an email
                send_mail(
                    subject='New Task Assigned',
                    message=f'Dear {task.employe},\n\nYou have been assigned a new task: {task.TaskName}.\n\nDue Date: {task.DueDate}\n\nPlease check your task management system for more details.',
                    from_email='adilfazal03@gmail.com',
                    recipient_list=[task.employe.email],
                )
    context = {'form': form}
    return render (request, 'accounts/update_task_status.html', context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def DeleteTask(request, pk):
    task = Tasks.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    context = {'task': task}
    return render (request, 'accounts/delete.html', context)
# Create your views here.


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
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

def project_detail(request, project_id):
    project = Projects.objects.get(id=project_id)
    return render(request, 'accounts/projects.html', {'project': project})