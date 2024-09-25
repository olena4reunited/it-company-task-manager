from django.urls import path

from task_manager.views import (
    Index,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
    TaskListView,
    WorkersListView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDetailView,
    WorkerDeleteView,
    TaskTypeListView,
    TaskTypeDetailView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    logout_confirmation
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="user-tasks"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("workers/", WorkersListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("tasktypes/", TaskTypeListView.as_view(), name="task-type-list"),
    path("tasktypes/<int:pk>/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("tasktypes/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("tasktypes/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path('logout/', logout_confirmation, name='logout-confirmation'),
]

app_name = "task-manager"