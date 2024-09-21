from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import TaskForm
from task_manager.models import Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.filter(is_completed=False).select_related("task_type").prefetch_related("assignees")

    paginator = Paginator(tasks, 7)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, template_name="task_manager/index.html", context=context)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task-manager:task-detail', args=[self.object.pk])


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees", "task_type")


@login_required
def task_set_completed(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.get(pk=pk)

    task.is_completed = True
    task.save()

    return redirect(reverse_lazy("task_manager:tasks"))


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:index")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:index")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/user_task_list.html"

    def get_queryset(self):
        return Task.objects.filter(is_completed=False).prefetch_related("assignees", "task_type").filter(assignees__contains=self.request.user)


class WorkersListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "task_manager/workers_list.html"
    context_object_name = "worker_list"
    paginate_by = 7

    def get_queryset(self):
        return get_user_model().objects.select_related("position").all()
