from django.contrib.auth import get_user_model
from datetime import date, time, timedelta
import pytest

from rest_framework.test import APIClient

from core.apps.duties.models import KitchenDuty
from core.apps.laundry.models import LaundryRecord
from core.apps.rooms.models import Block, Room, RoomRecord
from core.apps.users.models import CustomUser


UserModel = get_user_model()


@pytest.fixture
def test_user():
    new_user = UserModel.objects.create(username="bebra")
    new_user.set_password("amogus")
    new_user.save()
    return new_user


@pytest.fixture
def user_for_client():
    user = UserModel.objects.create(username="client_user")
    user.set_password("amogus")
    user.save()
    return user


@pytest.fixture
def user_client(client, user_for_client):
    new_client = client
    new_client.login(username="client_user", password="amogus")
    return new_client


@pytest.fixture
def test_laundry_records():
    today_date = date.today()
    records = []

    for hour in range(8, 21):
        records.append(
            LaundryRecord.objects.create(
                record_date=today_date,
                time_start=time(hour=hour, minute=0),
                time_end=time(hour=hour + 1, minute=0),
            )
        )
    # Вчерашняя запись
    records[0].record_date = today_date - timedelta(days=1)
    records[0].save()
    return records


@pytest.fixture
def test_room(user_for_client):
    block = Block.objects.create(floor=1)
    room = Room.objects.create(number="123", block=block)
    user_for_client.room = room
    user_for_client.save()
    # Dorm.objects.create(
    #     user=user_for_client,
    #     room=room
    # )
    return room


@pytest.fixture
def test_room_records(test_room, admin_user):
    room_records = []
    for i in range(2, 6):
        room_records.append(
            RoomRecord.objects.create(grade=i, room=test_room, author=admin_user)
        )
    return room_records


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(admin_user)
    return client


@pytest.fixture
def test_rooms_block():
    block = Block.objects.create(floor=1)
    return block


@pytest.fixture
def test_user_for_duty():
    user_for_duty = CustomUser.objects.create(
        username="user_for_duty_1", password="123"
    )
    return user_for_duty


@pytest.fixture
def test_user_not_in_duty():
    user_not_in_duty = CustomUser.objects.create(username="user_not_in_duty")
    return user_not_in_duty


@pytest.fixture
def test_duty(test_user_for_duty):
    duty = KitchenDuty.objects.create(date=date.today())
    duty.people.add(test_user_for_duty)
    return duty
