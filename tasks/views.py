# Add all your views here
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task


def task_view(request):
    search_term = request.GET.get("search")
    all_tasks = Task.objects.filter(deleted=False)
    tasks = all_tasks.filter(completed=False)
    completed_tasks = all_tasks.filter(completed=True)
    if search_term:
        tasks = tasks.filter(title__icontains=search_term)
        completed_tasks = completed_tasks.filter(title__icontains=search_term)
    return render(
        request, "tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
    )


def add_task(request):
    task_value = request.GET.get("task")
    # Task(title=task_value).save()
    task_obj = Task(title=task_value)
    task_obj.save()
    return HttpResponseRedirect("/")


def delete_task(request, index):
    # Task.objects.filter(id=index).delete()
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/")


def complete_task(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/")


def complete_task_view(request):
    completed_tasks = Task.objects.filter(deleted=False, completed=True)
    return render(request, "completed_tasks.html", {"completed_tasks": completed_tasks})


def all_tasks(request):
    all_tasks = Task.objects.filter(deleted=False)
    tasks = all_tasks.filter(completed=False)
    completed_tasks = all_tasks.filter(completed=True)
    return render(
        request, "all_tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
    )


def pending_tasks(request):
    tasks = Task.objects.filter(deleted=False, completed=False)
    return render(
        request,
        "pending_tasks.html",
        {"tasks": tasks},
    )
