from datetime import timedelta
from django.utils import timezone
from celery import shared_task

from core.apps.duties.services import generate_duty_schedule


@shared_task
def create_duty_schedule():
    date_start = timezone.now().date() + timedelta(days=7)
    date_end = date_start + timedelta(days=6)
    generate_duty_schedule(date_start=date_start, date_end=date_end)
