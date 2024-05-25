from datetime import date, timedelta
from core.apps.duties.models import KitchenDuty
from core.apps.duties.services import generate_duty_schedule
import pytest


@pytest.mark.django_db
def test_generate_schedule_success(test_users_with_rooms, default_duties_config):
    """
    Тестирует успешную генерацию графиков дежурств.
    """
    today = date.today()
    start = today
    end = today + timedelta(days=3)
    generate_duty_schedule(start, end)

    assert KitchenDuty.objects.count() == 4


@pytest.mark.django_db
def test_generate_schedule_success_circular(
    test_users_with_rooms, default_duties_config
):
    """
    Тестирует случай, когда генерация успешно выбирает проживающих по второму кругу.
    """
    today = date.today()
    start = today
    end = today + timedelta(days=13)
    generate_duty_schedule(start, end)

    assert KitchenDuty.objects.count() == 14


@pytest.mark.django_db
def test_generate_schedule_success_with_duties_count_priority(
    test_users_with_rooms, test_user_with_finished_duties, default_duties_config
):
    """
    Тестирует случай, когда проживающему с большим количеством завершенных дежурств не присваивается дежурство.
    """
    assert (
        test_user_with_finished_duties.kitchen_duties.filter(finished=True).count()
        == 10
    )

    today = date.today()
    start = today
    end = today + timedelta(days=6)
    generate_duty_schedule(start, end)

    assert KitchenDuty.objects.count() == 7 + 10
    assert (
        test_user_with_finished_duties.kitchen_duties.filter(finished=True).count()
        == 10
    )
