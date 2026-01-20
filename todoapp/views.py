from django.utils import timezone
now = timezone.now().strftime("%Y-%m-%d %H:%M")

from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
from .models import Tasks
from .forms import TasksForm, RegisterForm

@login_required(login_url='login')
def home_view(request):
    tasks = reversed(Tasks.objects.filter(user=request.user, status=0))
    form = TasksForm()

    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Привязываем юзера "под капотом"
            task.save()
            return redirect('home')

    context = {'tasks': tasks, 'form': form}

    return render(request, 'todoapp/home.html', context)
@login_required(login_url='login')
def completed_view(request):
    tasks = Tasks.objects.filter(user=request.user, status=1) | Tasks.objects.filter(user=request.user, status=2)

    return render(request, 'todoapp/completed_tasks.html', {'tasks':tasks})

def task_delete_view(request, task_id):
    referer = request.META.get('HTTP_REFERER')

    task = Tasks.objects.get(task_id=task_id)
    if request.method == 'POST':
        task.delete()
    return redirect(referer)
def task_complete_view(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    if request.method == 'POST':
        task.status = 1
        task.date_of_completion = now
        task.save()
    return redirect('home')
def task_dump_view(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    if request.method == 'POST':
        task.status = 2
        task.date_of_completion = now
        task.save()
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})
def login_view(request):
    error_message = ''

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'error_message': error_message, 'form': form})
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

