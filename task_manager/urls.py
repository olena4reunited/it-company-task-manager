from django.urls import path

from task_manager.views import index, TaskCreateView, TaskUpdateView, TaskDetailView, TaskDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]

app_name = "task-manager"
