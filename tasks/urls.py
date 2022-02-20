from django.urls import path
from tasks.views import (
    complete_task,
    GenericTaskView,
    GenericTaskCreateView,
    GenericTaskUpdateView,
    GenericTaskDetailView,
    GenericTaskDeleteView,
    login,
    signup,
)


urlpatterns = [
    path("", GenericTaskView.as_view()),
    path("add-task/", GenericTaskCreateView.as_view(), name="add-task"),
    # path("delete-task/<int:index>/", delete_task, name="delete-task"),
    path("complete_task/<int:index>/", complete_task),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view(), name="update-task"),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view(), name="detail-task"),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view(), name="delete-task"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
]
