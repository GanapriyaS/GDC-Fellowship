from django.urls import path
from tasks.views import (
    delete_task,
    all_tasks,
    complete_task_view,
    complete_task,
    pending_tasks,
    GenericTaskView,
    CreateTaskView,
)

urlpatterns = [
    path("", GenericTaskView.as_view()),
    path("add-task/", CreateTaskView.as_view(), name="add-task"),
    path("delete-task/<int:index>/", delete_task, name="delete-task"),
    path("completed_tasks/", complete_task_view, name="completed_tasks"),
    path("complete_task/<int:index>/", complete_task),
    path("all_tasks/", all_tasks, name="all_tasks"),
    path("tasks/", pending_tasks, name="tasks"),
]
