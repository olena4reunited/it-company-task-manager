from django import forms

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
