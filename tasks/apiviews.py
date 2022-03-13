from django.contrib.auth.models import User
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFromToRangeFilter,
    DjangoFilterBackend,
    FilterSet,
    ModelChoiceFilter,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from tasks.models import StatusHistory, Task

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)

# filter tasks


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)
    completed = BooleanFilter()


# Nested serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskSerializer(ModelSerializer):

    # user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "created_date",
            "completed",
            "user",
        ]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = {
        IsAuthenticated,
    }

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Status history


class StatusHistorySerializer(ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = "__all__"


class StatusHistoryFilter(FilterSet):
    timestamp = DateFromToRangeFilter()
    old_status = ChoiceFilter(choices=STATUS_CHOICES)
    new_status = ChoiceFilter(choices=STATUS_CHOICES)
    # task = ModelChoiceFilter(queryset=Task.objects.filter(deleted=False))


class StatusHistoryViewSet(ReadOnlyModelViewSet):
    queryset = StatusHistory.objects.all()
    serializer_class = StatusHistorySerializer

    permission_classes = {
        IsAuthenticated,
    }

    filter_backends = (DjangoFilterBackend,)
    filterset_class = StatusHistoryFilter

    def get_queryset(self, *args, **kwargs):
        task_id = self.kwargs.get("task__pk")
        if task_id:
            return self.queryset.filter(task__id=task_id, task__user=self.request.user)
        else:
            return self.queryset.filter(task__user=self.request.user)
