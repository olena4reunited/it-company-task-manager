from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import TaskForm, WorkerCreationForm, WorkerUpdateForm, TaskTypeForm
from task_manager.models import Task, Worker, TaskType


@login_required()
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


class WorkerCreateView(generic.CreateView):
    form_class = WorkerCreationForm
    template_name = 'task_manager/worker_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form)


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = 'task_manager/worker_update_form.html'
    success_url = reverse_lazy('task-manager:worker-list')


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = 'task_manager/worker_detail.html'
    context_object_name = 'worker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.prefetch_related('assignees').filter(assignees_contains=self.object)
        return context


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = 'task_manager/worker_confirm_delete.html'
    success_url = reverse_lazy('task-manager:workers-list')


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = 'task_manager/tasktype_list.html'
    context_object_name = 'tasktype_list'


class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    template_name = 'task_manager/tasktype_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('task_set')


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = 'task_manager/tasktype_update.html'
    context_object_name = 'tasktype'
    success_url = reverse_lazy('task-manager:tasktype-list')


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = 'task_manager/tasktype_confirm_delete.html'
    context_object_name = 'tasktype'
    success_url = reverse_lazy('task-manager:tasktype-list')
