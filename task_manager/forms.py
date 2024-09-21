from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.models import Worker, Task


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    deadline = forms.DateTimeField()

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "task_type", "assignees"]

    def save(self, commit=True, user=None):
        task = super().save(commit=False)
        if user is not None:
            task.created_by = user
        if commit:
            task.save()
        return task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position', 'password1', 'password2']


class WorkerUpdateForm(UserChangeForm):
    class Meta:
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position']

