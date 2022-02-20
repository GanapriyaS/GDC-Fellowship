from django.urls import path
from tasks.views import (
    complete_task,
    GenericTaskView,
    GenericTaskCreateView,
    GenericTaskUpdateView,
    GenericTaskDetailView,
    GenericTaskDeleteView,
    session_storage_view,
    UserCreateView,
    UserLoginView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", GenericTaskView.as_view()),
    path("add-task/", GenericTaskCreateView.as_view(), name="add-task"),
    path("complete_task/<int:index>/", complete_task),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view(), name="update-task"),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view(), name="detail-task"),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view(), name="delete-task"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("sessiontest/", session_storage_view),
    path("user/signup/", UserCreateView.as_view(), name="signup"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
]
