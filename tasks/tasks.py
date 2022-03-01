import imp
import time

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from tasks.models import Task
from datetime import timedelta

from celery.task import periodic_task
from task_manager.celery import app


@periodic_task(run_every=timedelta(seconds=10))
def send_email_remainder():
    for user in User.objects.all():
        pending_qs = Task.objects.filter(user=user, completed=False, deleted=False)
        email_content = f"You have {pending_qs.count()} pending tasks"
        send_mail(
            "Pending Tasks from Tasks Manager",
            email_content,
            "tasks@task_manager.org",
            [user.email],
        )
        print(f"Completed Processing User {user.id}")


# registered in celery to run background synchronouslys
@app.task
def test_background_jobs():
    print("THis is from the bg")
    for i in range(10):
        time.sleep(1)
        print(i)


# # in url.py or views.py
# def test_bg(request):
#     test_background_jobs.delay()
#     # delay() used to make background task
#     return HttpResponse("here good")
