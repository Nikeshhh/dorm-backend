import pytest

from core.apps.duties.exceptions import DutyIsLockedException, DutySwapException
from core.apps.duties.services import KitchenDutyService
from core.apps.users.models import CustomUser


@pytest.mark.django_db
def test_swap_pupils_success(test_duty, test_user_for_duty, test_user):
    """Тестирует успешную замену дежурного"""
    user_to_swap = test_user

    assert test_user_for_duty in test_duty.people.all()
    assert user_to_swap not in test_duty.people.all()

    duty_service = KitchenDutyService(test_duty)
    duty_service.swap_pupils(test_user_for_duty, user_to_swap)
    test_duty.refresh_from_db()

    assert test_user_for_duty not in test_duty.people.all()
    assert user_to_swap in test_duty.people.all()


@pytest.mark.django_db
def test_swap_pupils_on_error_on_finished(test_duty, test_user_for_duty, test_user):
    """Тестирует ошибку замену на оконченном дежурстве"""
    user_to_swap = test_user
    test_duty.finish()

    assert test_user_for_duty in test_duty.people.all()
    assert user_to_swap not in test_duty.people.all()

    duty_service = KitchenDutyService(test_duty)

    with pytest.raises(DutyIsLockedException):
        duty_service.swap_pupils(test_user_for_duty, user_to_swap)
    test_duty.refresh_from_db()

    assert test_user_for_duty in test_duty.people.all()
    assert user_to_swap not in test_duty.people.all()


@pytest.mark.django_db
def test_swap_pupils_on_error_no_match(test_duty, test_user_not_in_duty, test_user):
    """Тестирует ошибку при замене дежурного, которого нет в дежурстве"""
    user_to_swap = test_user

    assert test_user_not_in_duty not in test_duty.people.all()
    assert user_to_swap not in test_duty.people.all()

    duty_service = KitchenDutyService(test_duty)

    with pytest.raises(DutySwapException):
        duty_service.swap_pupils(test_user_not_in_duty, user_to_swap)
    test_duty.refresh_from_db()

    assert test_user_not_in_duty not in test_duty.people.all()
    assert user_to_swap not in test_duty.people.all()


@pytest.mark.django_db
def test_swap_pupils_on_error_already_in_duty(test_duty):
    """Тестирует ошибку при замене на дежурного, который итак уже в дежурстве"""
    current_user = CustomUser.objects.get(username="user_for_duty_1")
    user_to_swap = CustomUser.objects.create(username="swapped_to_user")
    test_duty.people.add(user_to_swap)

    assert current_user in test_duty.people.all()
    assert user_to_swap in test_duty.people.all()

    duty_service = KitchenDutyService(test_duty)

    with pytest.raises(DutySwapException):
        duty_service.swap_pupils(current_user, user_to_swap)
    test_duty.refresh_from_db()

    assert current_user in test_duty.people.all()
    assert user_to_swap in test_duty.people.all()
