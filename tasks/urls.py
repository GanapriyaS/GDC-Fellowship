from django.urls import path, include
from tasks.views import (
    complete_task,
    GenericTaskView,
    GenericTaskCreateView,
    GenericTaskUpdateView,
    GenericTaskDetailView,
    GenericTaskDeleteView,
    UserCreateView,
    UserLoginView,
)
from tasks.apiviews import TaskViewSet, StatusHistoryViewSet
from django.contrib.auth.views import LogoutView

from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter

router = routers.SimpleRouter()
router.register("api/task", TaskViewSet)
router.register("api/history", StatusHistoryViewSet, basename="history")

nested_router = routers.NestedSimpleRouter(router, r"api/task", lookup="task")
nested_router.register(r"history", StatusHistoryViewSet)

# https://medium.com/swlh/using-nested-routers-drf-nested-routers-in-django-rest-framework-951007d55cdc
urlpatterns = [
    path("", GenericTaskView.as_view()),
    path("add-task/", GenericTaskCreateView.as_view(), name="add-task"),
    path("complete_task/<int:index>/", complete_task),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view(), name="update-task"),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view(), name="detail-task"),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view(), name="delete-task"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/signup/", UserCreateView.as_view(), name="signup"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path("", include(nested_router.urls)),
] + router.urls
