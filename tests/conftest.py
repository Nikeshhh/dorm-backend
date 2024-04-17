from django.contrib.auth import get_user_model
from datetime import date, time, timedelta
import pytest

from core.apps.laundry.models import LaundryRecord


UserModel = get_user_model()


@pytest.fixture
def test_user():
    new_user = UserModel.objects.create(username='bebra')
    new_user.set_password('amogus')
    new_user.save()
    return new_user


@pytest.fixture
def user_client(client):
    user = UserModel.objects.create(username='client_user')
    user.set_password('amogus')
    user.save()
    
    new_client = client
    new_client.login(username='client_user', password='amogus')
    return new_client


@pytest.fixture
def test_laundry_records():
    today_date = date.today()
    records = []

    for hour in range(8, 21):
        records.append(LaundryRecord.objects.create(
            record_date=today_date,
            time_start=time(hour=hour, minute=0),
            time_end=time(hour=hour+1, minute=0)
        ))
    # Вчерашняя запись
    records[0].record_date = today_date - timedelta(days=1)
    records[0].save()
    return records