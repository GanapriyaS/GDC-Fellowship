from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

tasks = []
completed_tasks = []


def task_view(request):
    return render(
        request, "tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
    )


def add_task(request):
    task_value = request.GET.get("task")
    tasks.append(task_value)
    return HttpResponseRedirect("/")


def delete_task(request, index):
    del tasks[index - 1]
    return HttpResponseRedirect("/")


def complete_task(request, index):
    completed_tasks.append(tasks[index - 1])
    del tasks[index - 1]
    return HttpResponseRedirect("/")


def complete_task_view(request):
    return render(request, "completed_tasks.html", {"completed_tasks": completed_tasks})


def all_tasks(request):
    return render(
        request, "all_tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
    )


def pending_tasks(request):
    return render(
        request,
        "pending_tasks.html",
        {"tasks": tasks, "tasks": tasks},
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
