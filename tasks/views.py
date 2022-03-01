# Add all your views here


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.http import HttpResponseRedirect

from tasks.forms import UserSignupForm, UserLoginForm, TaskCreateForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from tasks.models import Task


# ==================================== USER VIEWS =================================

# Customising Login page
class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)


# Login feature
class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = UserLoginForm


# Register an user
class UserCreateView(CreateView):
    form_class = UserSignupForm
    template_name = "signup.html"
    success_url = "/user/login"


# ================================ TASK VIEWS ================================

# function to cascade the priority
def cascade_priority(temp, user, id):
    tasks = Task.objects.filter(
        deleted=False,
        user=user,
        completed=False,
    ).exclude(id=id)
    task = tasks.filter(priority=temp).first()

    if task:
        changes = []
        while task:
            task.priority = temp + 1
            changes.append(task)
            temp += 1
            task = tasks.filter(priority=temp).first()
        Task.objects.bulk_update(changes, ["priority"])


# To update a tasks
class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):

    form_class = TaskCreateForm
    template_name = "update.html"
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save()

        if not self.object.completed:
            cascade_priority(self.object.priority, self.request.user, self.object.id)

        # self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# Create a new task
class GenericTaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = "add.html"
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save()

        if not self.object.completed:
            cascade_priority(self.object.priority, self.request.user, self.object.id)

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
