from datetime import timedelta, date
from django.shortcuts import render, redirect
from django.shortcuts import render
from . import models
from .forms import TaskForm
from .models import Task
from django.db.models import Count
from django import forms
from django.contrib.auth.decorators import login_required
import pandas as pd


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user_email', 'task', 'due_by', 'priority', 'is_urgent']


@login_required
def add_task(request):
    if request.method == 'POST':
        print("POST request received")
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form is valid, task saved")
            return redirect('landing')  # Redirect after saving
        else:
            print("Form is invalid")
    else:
        print("GET request received")
        form = TaskForm()

    return render(request, 'tasks/add_task.html', {'form': form})

def landing_page(request):
    return render(request, 'tasks/landing.html')


def dashboard(request):
    today = date.today()
    thirty_days_from_now = today + timedelta(days=30)

    # Query tasks due in the next 30 days
    tasks_due_soon = Task.objects.filter(due_by__range=[today, thirty_days_from_now])

    # Number of urgent tasks due in the next 30 days
    urgent_tasks_count = tasks_due_soon.filter(is_urgent=True).count()

    # Data for line chart
    daily_tasks = tasks_due_soon.values('due_by').annotate(count=Count('id')).order_by('due_by')
    daily_tasks_df = pd.DataFrame(list(daily_tasks))
    if not daily_tasks_df.empty:
        daily_tasks_df['due_by'] = daily_tasks_df['due_by'].dt.strftime('%Y-%m-%d')
    daily_tasks_data = daily_tasks_df.to_dict(orient='records')

    # Data for pie chart
    priority_counts = tasks_due_soon.values('priority').annotate(count=Count('id'))
    priority_counts_df = pd.DataFrame(list(priority_counts))
    priority_counts_data = priority_counts_df.to_dict(orient='records')

    context = {
        'tasks_due_soon': tasks_due_soon,
        'urgent_tasks_count': urgent_tasks_count,
        'daily_tasks': daily_tasks_data,
        'priority_counts': priority_counts_data,
    }

    return render(request, 'tasks/dashboard.html', context)
