from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, Position, Worker, Task

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'position')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {
            "fields": (
                "position",
            )
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deadline', 'is_completed', 'priority', 'task_type', 'created_by')
    search_fields = ('name', )
    list_filter = ('is_completed', 'priority', 'task_type')
    ordering = ('-deadline',)
    autocomplete_fields = ('assignees',)

