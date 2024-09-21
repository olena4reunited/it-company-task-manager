from django.urls import path

from task_manager.views import index, TaskCreateView

urlpatterns = [
    path("", index, name="index"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
]

app_name = "task-manager"
