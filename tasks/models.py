from django.db import models

class Task(models.Model):
    user_email = models.EmailField()
    task = models.CharField(max_length=255)
    due_by = models.DateField()
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.task