from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from tasks.models import Task, Report
from datetime import timedelta
from datetime import datetime, date
from celery.task import periodic_task
from task_manager.celery import app


@periodic_task(run_every=timedelta(seconds=10))
def send_email_remainder():
    now = datetime.now().strftime("%H:%M")
    print(now)
    today = date.today()

    # https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q
    for report in Report.objects.filter(remainder_time__lte=now, disabled=False).filter(
        ~Q(last_day=today)
    ):
        user = User.objects.get(id=report.user.id)
        all_tasks = Task.objects.filter(deleted=False, user__id=report.user.id)

        pending_count = all_tasks.filter(status="0").count()
        in_progress_count = all_tasks.filter(status="1").count()
        completed_count = all_tasks.filter(status="2").count()
        cancelled_count = all_tasks.filter(status="3").count()

        content = f" {pending_count} pending tasks\n {in_progress_count} in-progress tasks {completed_count} Completed tasks \n and {cancelled_count} Cancelled tasks"
        send_mail("Daily Status Report", content, "tasks@taskmanager.org", [user.email])
        print(f"User {user.username} **** Email: {user.email}")
        print("Email received")
        report.last_day = today
        report.save()
