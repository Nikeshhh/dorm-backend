from datetime import date, time
from django.db.transaction import atomic

from core.apps.laundry.models import LaundryRecord


def create_laundry_records_for_today():
    today = date.today()
    with atomic():
        for hour in range(8, 22):
            LaundryRecord.objects.create(
                record_date=today,
                time_start=time(hour=hour, minute=0),
                time_end=time(hour=hour + 1, minute=0),
            )
