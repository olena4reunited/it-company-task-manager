from django.urls import path

from task_manager.views import index, TaskCreateView, TaskUpdateView, TaskDetailView, TaskDeleteView, TaskListView, \
    WorkersListView, task_set_completed, WorkerCreateView, WorkerUpdateView, WorkerDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="user-tasks"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/complete/", task_set_completed, name="task-set-completed"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("workers/", WorkersListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
]

app_name = "task-manager"
