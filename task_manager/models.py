from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SET_NULL


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    name = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=63,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )
