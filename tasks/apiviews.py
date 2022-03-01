from tasks.models import Task
from django.contrib.auth.models import User

from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    ChoiceFilter,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.serializers import ModelSerializer, Serializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)


# Nested serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "created_date",
            "completed",
            "user",
        ]


# class TaskSerializer(Serializer):
#     task = serializer.CharField(max_length=100)
#     description = serializer.CharField()

#     def create(self, validated_data):
#         title = validated_data.get("title")
#         description = validated_data.get("description")
#         return Task(title=title, description=description)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.description = validated_data.get("description", instance.description)
#         return instance


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


# serialize


class TaskListAPI(APIView):
    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        data = TaskSerializer(tasks, many=True).data
        return Response({"tasks": data})


# class TaskListAPI(APIView):
#     def get(self, request):
#         tasks = Task.objects.filter(deleted=False)
#         data = []
#         for task in tasks:
#             data.append({"title": task.title})
#         return Response({"tasks": data})
