from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, Tag, Task, TaskType, Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                )
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "get_tags",
    )
    list_filter = ("is_completed", "priority", "task_type", "tags")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees", "tags")

    @admin.display(description="Tags")
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()]) or "-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
