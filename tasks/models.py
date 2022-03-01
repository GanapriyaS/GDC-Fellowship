from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

STATUS_CHOICES = (
    ("0", "PENDING"),
    ("1", "IN_PROGRESS"),
    ("2", "COMPLETED"),
    ("3", "CANCELLED"),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(default="1")
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class StatusHistory(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    old_status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True)
    new_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.title


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    remainder_time = models.TimeField()
    last_day = models.DateField(null=True, default=None, blank=True)
    disabled = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# https://docs.djangoproject.com/en/4.0/topics/signals/
@receiver(pre_save, sender=Task)
def handler(sender, instance, **kwargs):
    print(instance)
    task = Task.objects.filter(id=instance.id).first()
    if task and task.status != instance.status:
        StatusHistory.objects.create(
            task=task, old_status=task.status, new_status=instance.status
        )
