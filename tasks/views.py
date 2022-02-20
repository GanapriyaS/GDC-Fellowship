# Add all your views here

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect


from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from tasks.models import Task


# ==================================== USER VIEWS =================================

# Customising Login page
class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Password",
            }
        )
    )


# Customising signup form
class UserSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Username",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Repeat password",
            }
        )


# Login feature
class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = UserLoginForm


# Register an user
class UserCreateView(CreateView):
    form_class = UserSignupForm
    template_name = "signup.html"
    success_url = "/user/login"


def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views + 1
    return HttpResponse(f"Total views is {total_views} and the user is {request.user}")


# ================================ TASK VIEWS ================================

# Form to get task details
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


# To update a tasks
class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "update.html"
    success_url = "/"


# Create a new task
class GenericTaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = "add.html"
    success_url = "/"

    def recursion(self, key, id):
        key = int(key)
        prior_task = Task.objects.filter(
            priority=key, deleted=False, user=self.request.user
        )
        if prior_task.exists():
            self.recursion(key + 1, prior_task[0].id)
        Task.objects.filter(id=id).update(priority=key)

    def form_valid(self, form):
        self.object = form.save()
        tasks = Task.objects.filter(
            deleted=False,
            user=self.request.user,
            priority=self.object.priority,
        )

        if tasks.exists():
            self.recursion(self.object.priority, tasks[0].id)
            Task.objects.filter(id=tasks[0].id).update(
                priority=int(self.object.priority) + 1
            )

        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# To detail view of tasks
class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "detail.html"


# To delete tasks
class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = "/"


# Listview of all tasks category wise
class GenericTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(GenericTaskView, self).get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("search")
        all_tasks = Task.objects.filter(deleted=False, user=self.request.user).order_by(
            "priority"
        )
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
        tasks = Task.objects.filter(deleted=False, user=self.request.user).order_by(
            "priority"
        )
        if search_term:
            tasks = tasks.filter(title__icontains=search_term).order_by("priority")
        return tasks


# To mark task as complete
def complete_task(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/")
