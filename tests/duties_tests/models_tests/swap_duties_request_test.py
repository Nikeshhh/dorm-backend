import pytest

from core.apps.duties.exceptions import DutySwapException
from core.apps.duties.models import SwapDutiesRequest


@pytest.mark.django_db
def test_swap_duties_accept_success(test_duties, test_users):
    """Успешный обмен дежурствами при принятии заявки"""
    user1, user2 = test_users[:2]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    swap_request = SwapDutiesRequest.objects.create(
        first_duty=duty1, first_user=user1, second_duty=duty2, second_user=user2
    )

    swap_request.accept(user2)

    duty1.refresh_from_db()
    duty2.refresh_from_db()

    assert user1 not in duty1.people.all()
    assert user1 in duty2.people.all()
    assert user2 not in duty2.people.all()
    assert user2 in duty1.people.all()


@pytest.mark.django_db
def test_swap_duties_decline_success(test_duties, test_users):
    """Успешное отклонение заявки с сохранением исходного состояния"""
    user1, user2 = test_users[:2]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    swap_request = SwapDutiesRequest.objects.create(
        first_duty=duty1, first_user=user1, second_duty=duty2, second_user=user2
    )

    swap_request.decline(user2)

    duty1.refresh_from_db()
    duty2.refresh_from_db()

    assert user1 in duty1.people.all()
    assert user1 not in duty2.people.all()
    assert user2 in duty2.people.all()
    assert user2 not in duty1.people.all()

    swap_request.refresh_from_db()
    assert swap_request.declined is True


@pytest.mark.django_db
def test_swap_duties_creation_error_same_duty(test_duties, test_users):
    """Успешное отклонение заявки с сохранением исходного состояния"""
    user1, user2 = test_users[:2]
    target_duty = user1.kitchen_duties.first()
    duty1 = duty2 = target_duty

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapDutiesRequest.objects.create(
            first_duty=duty1, first_user=user1, second_duty=duty2, second_user=user2
        )

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()


@pytest.mark.django_db
def test_swap_duties_error_same_user(test_duties, test_users):
    """Успешное отклонение заявки с сохранением исходного состояния"""
    user1 = user2 = test_users[0]
    duty1, duty2 = test_duties[0], test_duties[1]

    with pytest.raises(DutySwapException):
        SwapDutiesRequest.objects.create(
            first_duty=duty1, first_user=user1, second_duty=duty2, second_user=user2
        )
