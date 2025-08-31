from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm
from .models import Task


def index(request):
    return render(request, 'todo/index.html')

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return  redirect('taskList')
    else:
        form = UserCreationForm()
    return render(request,"todo/register.html",{'form':form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = user,password = password)
            if user is not None:
                login(request,user)
                return redirect('taskList')
            else:
                messages.error(request,"Login yoki Parol xato kiritilgan")
        else:
            messages.error(request,"Login yoki Parol xato kiritilgan")
    else:
        form = AuthenticationForm()
    return render(request,"todo/login.html",{'form':form})

@login_required
def taskList(request):
    tasks = Task.objects.filter(user = request.user)
    return render(request,'todo/tasklist.html',{'tasks':tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('taskList')
    else:
        form = TaskForm()
    return render(request,'todo/taskform.html',{'form':form})

@login_required
def task_update(request,update_id):
    task = get_object_or_404(Task,pk = update_id,user = request.user)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('taskList')
    else:
        form = TaskForm(instance=task)
    return render(request,'todo/taskform.html',{'form':form})

@login_required
def task_delete(request,delete_id):
    task = get_object_or_404(Task,pk = delete_id,user = request.user)
    if request.method == "POST":
        task.delete()
        return redirect('taskList')
    return render(request,'todo/taskdelete.html',{'task':task})

def user_logout(request):
    logout(request)
    return redirect("login")

