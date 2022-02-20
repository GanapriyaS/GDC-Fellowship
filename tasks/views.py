# Add all your views here
from turtle import pen
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


from tasks.models import Task


class TaskCreateForm(ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 10:
            raise ValidationError("Data too small")
        return title.upper()

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "completed"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget.attrs.update(
            {
                "rows": "1",
                "placeholder": "Description",
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["title"].widget.attrs.update(
            {
                "placeholder": "Title",
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["priority"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["completed"].widget.attrs.update(
            {
                "class": "ml-2 mb-4 focus:outline-none",
            }
        )


class GenericTaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "update.html"
    success_url = "/"


class GenericTaskCreateView(CreateView):
    form_class = TaskCreateForm
    template_name = "add.html"
    success_url = "/"


class GenericTaskDetailView(DetailView):
    model = Task
    template_name = "detail.html"


class GenericTaskDeleteView(DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = "/"


# class GenericTaskCreateView(CreateView):
#     model = Task
#     fields = ("title", "description", "completed")
#     template_name = "tasks.html"
#     success_url = "/"


class GenericTaskView(ListView):
    # model = Task
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(GenericTaskView, self).get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("search")
        all_tasks = Task.objects.filter(deleted=False)
        if search_term:
            all_tasks = all_tasks.filter(title__icontains=search_term)
        pending = all_tasks.filter(completed=False)
        completed = all_tasks.filter(completed=True)
        context["all"] = all_tasks
        context["pending"] = pending
        context["completed"] = completed

        return context

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False)
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks


class CreateTaskView(ListView):
    def get(self, request):
        return render(request, "tasks.html")

    def post(self, request):
        task_value = request.POST.get("task")
        task_obj = Task(title=task_value)
        task_obj.save()
        return HttpResponseRedirect("/")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


# class TaskView(View):
#     def get(self, request):
#         search_term = request.GET.get("search")
#         all_tasks = Task.objects.filter(deleted=False)
#         tasks = all_tasks.filter(completed=False)
#         completed_tasks = all_tasks.filter(completed=True)
#         if search_term:
#             tasks = tasks.filter(title__icontains=search_term)
#             completed_tasks = completed_tasks.filter(title__icontains=search_term)
#         return render(
#             request, "tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
#         )

#     def post(self, request):
#         pass


# def add_task(request):
#     task_value = request.GET.get("task")
#     # Task(title=task_value).save()
#     task_obj = Task(title=task_value)
#     task_obj.save()
#     return HttpResponseRedirect("/")


def complete_task(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/")
