from datetime import date, timedelta
from core.apps.duties.models import KitchenDuty, KitchenDutyConfig
from core.apps.duties.services import generate_duty_schedule
import pytest

from core.apps.rooms.models import Room
from core.apps.users.models import CustomUser


@pytest.mark.django_db
def test_generate_schedule_success(test_rooms_block):
    KitchenDutyConfig.objects.create(people_per_day=2)
    for i in range(10):
        room = Room.objects.create(number=str(i), block=test_rooms_block)
        CustomUser.objects.create(username=f"bebra#{i}", room=room)

    today = date.today()
    start = today
    end = today + timedelta(days=3)
    generate_duty_schedule(start, end)

    assert KitchenDuty.objects.count() == 4


# TODO: сделать тесты, где у людей уже есть завершенные дежурства
