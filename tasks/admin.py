from django.contrib import admin

# Register your models here.
from .models import Task
from .models import StatusHistory, Report

admin.sites.site.register(Task)
admin.sites.site.register(StatusHistory)
admin.sites.site.register(Report)
