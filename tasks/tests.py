from django.contrib.auth.models import User

from json import loads

from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory
from .views import (
    GenericTaskCreateView,
    GenericTaskView,
    GenericTaskDeleteView,
    GenericTaskUpdateView,
    complete_task,
)
from .models import Task, StatusHistory, Report
from .tasks import send_email_remainder
from datetime import datetime
from io import StringIO
from unittest.mock import patch
from rest_framework.test import force_authenticate
from .apiviews import TaskViewSet, StatusHistoryViewSet


class QuestionModelTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.apifactory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman"
        )

    def test_authenticated(self):
        """
        Try to GET the tasks listing page, expect the response to redirect to the login page
        """
        endpoints = [
            "/",
            "/add-task/",
        ]

        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, f"/user/login?next={endpoint}")

        api_endpoints = [
            "/api/task/",
            "/api/history/",
        ]

        for endpoint in api_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 403)

    # To check login page
    def login(self, username, password):
        response = self.client.post(
            "/user/login/", {"username": "bruce_wayne", "password": "i_am_batman"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    # To check veiw page works fine
    def test_task_view(self):
        """
        Try to GET the tasks listing page, expect the response to redirect to the login page
        """
        # Create an instance of a GET request.
        request = self.factory.get("/")
        # Set the user instance on the request.
        request.user = self.user
        # We simply create the view and call it like a regular function
        response = GenericTaskView.as_view()(request)
        # Since we are authenticated we get a 200 response
        self.assertEqual(response.status_code, 200)

    # To test delete functionality
    def test_task_delete(self):
        task_name = "Do web development"

        task = Task(
            title=task_name,
            description="Daily Task",
            priority=1,
            status="P",
            completed=False,
            user=self.user,
        )
        task.save()

        request = self.factory.delete("/delete-task")
        # Set the user instance on the request.
        request.user = self.user
        # We simply create the view and call it like a regular function
        response = GenericTaskDeleteView.as_view()(request, pk=task.id)
        self.assertEqual(response.status_code, 302)

    # To test update functionality
    def test_task_update(self):
        task_name = "Do web development"

        task = Task(
            title=task_name,
            description="Daily Task",
            priority=1,
            status="0",
            completed=False,
            user=self.user,
        )
        task.save()
        task_update = {
            "status": "0",
            "completed": True,
            "title": "cascade",
            "description": "des",
            "priority": 5,
            "user": self.user,
        }
        request = self.factory.post(f"/update-task/{task.id}", data=task_update)
        request.user = self.user
        response = GenericTaskUpdateView.as_view()(request, pk=task.id)
        self.assertEqual(response.status_code, 302)

    # To test logout functionalitys
    def logout(self):
        response = self.client.get("/user/logout/")
        self.assertEqual(response.url, "/user/login")
        self.assertEqual(response.status_code, 302)

    # Test for creating tasks
    def test_create_task(self):
        task = {
            "status": "0",
            "completed": True,
            "title": "cascade",
            "description": "des",
            "priority": 5,
            "user": self.user,
        }

        request = self.factory.post("/add-task", data=task)
        request.user = self.user
        response = GenericTaskCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.filter(user=self.user).first().title, "CASCADE")

    # Test to check cascading
    def test_task_cascade(self):
        task = {
            "status": "0",
            "completed": False,
            "title": "cascade",
            "description": "des",
            "priority": 5,
            "user": self.user,
        }

        request = self.factory.post("/add-task", data=task)
        request.user = self.user
        GenericTaskCreateView.as_view()(request)
        request = self.factory.post("/add-task", data=task)
        request.user = self.user
        GenericTaskCreateView.as_view()(request)
        self.assertEqual(Task.objects.get(id=1).priority, 6)

    # Test to check task api
    def test_api_tasks(self):
        task = Task(
            title="api get test",
            description="des",
            priority=5,
            user=self.user,
            completed="False",
            status="0",
        ).save()

        request = self.apifactory.get("/api/task")
        force_authenticate(request, user=self.user)
        view = TaskViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    # To check email working
    def test_email_report(self):
        report = Report(
            remainder_time=datetime.now().strftime("%H:%M"),
            user=self.user,
            disabled=False,
        )
        report.save()
        report_email = send_email_remainder()
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertIn(out.getvalue(), "bruce@wayne.org")
        self.assertTrue(report_email, msg="Email received")

    # To test complete marking functionality
    def test_completed_tasks(self):
        task_name = "Do web development"

        task = Task(
            title=task_name,
            description="Daily Task",
            priority=1,
            status="0",
            completed=False,
            user=self.user,
        )
        task.save()

        request = self.factory.get(f"/complete_task/{task.id}")
        request.user = self.user
        complete_task(self, task.id)
        task = Task.objects.filter(user=self.user).first()
        self.assertTrue(task.completed)

    # Testing history functionality
    def test_history_generation(self):
        task_name = "Do web development"

        task = Task(
            title=task_name,
            description="Daily Task",
            priority=1,
            status="0",
            completed=False,
            user=self.user,
        )
        task.save()
        task_update = {
            "status": "1",
            "completed": True,
            "title": task_name,
            "description": "des",
            "priority": 5,
            "user": self.user,
        }
        request = self.factory.post(f"/update-task/{task.id}", data=task_update)
        request.user = self.user
        response = GenericTaskUpdateView.as_view()(request, pk=task.id)
        self.assertEqual(response.status_code, 302)

        request = self.apifactory.get("/api/history")
        force_authenticate(request, user=self.user)
        request.user = self.user
        view = StatusHistoryViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        history = StatusHistory.objects.filter(task=task.id).last()
        self.assertEqual(history.old_status, "0")
        self.assertEqual(history.new_status, "1")

    # To check nested routers
    def test_nested_routers(self):
        self.test_history_generation()
        task = StatusHistory.objects.first().task
        self.login(username="bruce_wayne", password="i_am_batman")
        history = loads(self.client.get(f"/api/task/{task.pk}/history/").content)
        self.assertEqual(len(history), StatusHistory.objects.filter(task=task).count())
        self.logout()
