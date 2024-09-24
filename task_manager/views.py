from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm, WorkerCreationForm, TaskTypeForm, WorkerUpdateForm
from task_manager.models import Task, TaskType

User = get_user_model()


class QuerySetOptimizeMixin:
    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self, 'select_related_fields'):
            queryset = queryset.select_related(*self.select_related_fields)
        if hasattr(self, 'prefetch_related_fields'):
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'model'):
            queryset = self.get_queryset()
            context[self.get_context_object_name(queryset)] = queryset
        return context


class Index(generic.TemplateView):
    template_name = "task_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.select_related('task_type').prefetch_related('assignees')[:10]
        context['task_types'] = TaskType.objects.all()[:10]
        context['team_members'] = User.objects.all()[:10]
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-manager:task-detail', kwargs={'pk': self.object.pk})


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    select_related_fields = ['assignees', 'task_type', 'created_by']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user in self.object.assignees.all() and not self.object.is_completed:
            self.object.is_completed = True
            self.object.save()
            return redirect('task-manager:task-detail', pk=self.object.pk)
        else:
            messages.error(request, "You don't have permission to complete this task.")
            return redirect('task-manager:task-detail', pk=self.object.pk)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-manager:user-tasks")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task-manager:user-tasks")


class TaskListView(LoginRequiredMixin, QuerySetOptimizeMixin, generic.ListView):
    model = Task
    template_name = "task_manager/user_task_list.html"
    context_object_name = 'tasks'
    select_related_fields = ['task_type', 'created_by']
    prefetch_related_fields = ['assignees']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('assignees').filter(assignees=self.request.user)
        return queryset


class WorkersListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "task_manager/workers_list.html"
    context_object_name = "worker_list"
    paginate_by = 7

    def get_queryset(self):
        return User.objects.select_related("position").all()

class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = WorkerCreationForm
    template_name = 'task_manager/worker_form.html'
    success_url = reverse_lazy('login')


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = WorkerUpdateForm
    template_name = 'task_manager/worker_update_form.html'
    success_url = reverse_lazy('task-manager:worker-list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user == self.get_object()


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'task_manager/worker_detail.html'
    context_object_name = 'worker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.prefetch_related('assignees').filter(assignees=self.object)
        return context


class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = User
    template_name = 'task_manager/worker_confirm_delete.html'
    success_url = reverse_lazy('task-manager:workers-list')

    def test_func(self):
        return self.request.user.is_staff


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = 'task_manager/tasktype_list.html'
    context_object_name = 'task_type_list'


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = 'task_manager/tasktype_detail.html'
    context_object_name = 'task_type'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tasks')


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = 'task_manager/tasktype_update.html'
    context_object_name = 'task_type'
    success_url = reverse_lazy('task-manager:task-type-list')


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = 'task_manager/tasktype_confirm_delete.html'
    context_object_name = 'task_type'
    success_url = reverse_lazy('task-manager:task-type-list')