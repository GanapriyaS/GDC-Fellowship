from django.urls import path
from tasks.views import (
    add_task,
    task_view,
    delete_task,
    complete_task_view,
    complete_task,
    all_tasks,
    pending_tasks,
)

urlpatterns = [
    path("", task_view),
    path("add-task/", add_task, name="add-task"),
    path("delete-task/<int:index>/", delete_task, name="delete-task"),
    path("completed_tasks/", complete_task_view, name="completed_tasks"),
    path("complete_task/<int:index>/", complete_task),
    path("all_tasks/", all_tasks, name="all_tasks"),
    path("tasks/", pending_tasks, name="tasks"),
]
