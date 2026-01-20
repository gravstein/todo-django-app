from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models

# Create your models here.
class Tasks(models.Model):
    class Status(models.IntegerChoices):
        UNCOMPLETED = 0,
        COMPLETED = 1,
        DUMPED = 2

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(
        choices = Status.choices,
        default = Status.UNCOMPLETED
    )

    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_completion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"The task {self.name} is {"uncompleted" if self.status == 0 else "completed" if self.status == 1 else "dumped"}"