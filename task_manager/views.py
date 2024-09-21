from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from task_manager.models import Task


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type").prefetch_related("assignees").filter("is_completed=False")

    context = {
        tasks: tasks,
    }

    return render(request=request, template_name="task_manager/index.html", context=context)



