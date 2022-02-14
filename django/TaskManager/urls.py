"""TaskManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# from django.http import Http404
task = []


def task_view(request):
    # return HttpResponse(status=404)
    # if True:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    # else:
    #     return HttpResponse('<h1>Page was found</h1>') or return HttpResponse("<h1>Hello</h1>", status=200)

    # to have a consistent 404 error page across your site, Django provides an Http404 exception. If you raise Http404 at any point in a view function, Django will catch it and return the standard error page for your application, along with an HTTP error code 404.
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404("Poll does not exist")
    # return render(request, "polls/detail.html", {"poll": p})
    return render(request, "index.html", {"task": task})


def add_task(request):
    task_value = request.GET.get("task")
    task.append(task_value)
    return HttpResponseRedirect("/task")


def delete_task(reques, index):
    del task[index - 1]
    return HttpResponseRedirect("/task")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("task/", task_view),
    path("add-task", add_task),
    path("delete-task/<int:index>", delete_task),
]
