from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.template.defaultfilters import first
from django.utils import timezone
from django_select2.forms import Select2MultipleWidget

from task_manager.models import Worker, Task, TaskType


class TaskForm(forms.ModelForm):
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        initial="medium",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "task_type", "assignees"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
            "deadline": forms.DateInput(
                attrs={"type": "date", "title": "Deadline"}
            ),
            "assignees": Select2MultipleWidget(attrs={"class": "form-control form-control-lg"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now().date():
            raise forms.ValidationError("Deadline must be in the future")
        return deadline

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "bform-control form-control-lg"
            else:
                field.widget.attrs.update({"class": "form-control form-control-lg"})

            if field_name in ("priority", "task_type"):
                field.widget.attrs["class"] += " form-select"

            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"


    def save(self, commit=True, user=None):
        task = super().save(commit=False)
        if user is not None:
            task.created_by = user
        if commit:
            task.save()
            self.save_m2m()
        return task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position', 'password1', 'password2']


class WorkerUpdateForm(UserChangeForm):
    class Meta:
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position']


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ['name']
