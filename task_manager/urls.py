from django.urls import path

from task_manager.views import index, TaskCreateView, TaskUpdateView, TaskDetailView, TaskDeleteView, TaskListView, \
    WorkersListView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="user-tasks"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("workers/", WorkersListView.as_view(), name="worker-list"),
]

app_name = "task-manager"
