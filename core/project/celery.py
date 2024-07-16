import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.project.settings")

app = Celery("dorm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["core.apps.reports"])
