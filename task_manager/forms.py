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
