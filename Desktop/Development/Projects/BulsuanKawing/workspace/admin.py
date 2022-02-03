from django.contrib import admin

from .models import Workspace, ToDoList, Task, TaskState


class TaskAdmin (admin.ModelAdmin):
    list_display = ('name', 'tdl_ID', 'time_begin', 'time_end')

    search_fields = ('name', 'tdl_ID__name', 'description')


class TodoAdmin (admin.ModelAdmin):
    list_display = ('wp_ID', 'name')
    search_fields = ('wp_ID', 'name')


admin.site.register(Workspace)
admin.site.register(ToDoList, TodoAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskState)

