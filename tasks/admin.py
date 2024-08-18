from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'task', 'due_by', 'priority', 'is_urgent')
