import pytest

from core.apps.duties.exceptions import DutySwapException
from core.apps.duties.models import SwapPeopleRequest


@pytest.mark.django_db
def test_swap_people_accept_success(test_duties, test_users):
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    swap_request = SwapPeopleRequest.objects.create(
        current_user=user1, to_swap=user2, duty=target_duty
    )

    swap_request.accept(user2)

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is True
    assert swap_request.declined is False
    assert swap_request.canceled is False


@pytest.mark.django_db
def test_swap_people_decline_success(test_duties, test_users):
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    swap_request = SwapPeopleRequest.objects.create(
        current_user=user1, to_swap=user2, duty=target_duty
    )

    swap_request.decline(user2)

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is False
    assert swap_request.declined is True
    assert swap_request.canceled is False


@pytest.mark.django_db
def test_swap_people_on_already_in_duty(test_duties, test_users):
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]
    target_duty.people.add(user2)

    assert user1 in target_duty.people.all()
    assert user2 in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapPeopleRequest.objects.create(
            current_user=user1, to_swap=user2, duty=target_duty
        )

    assert user1 in target_duty.people.all()
    assert user2 in target_duty.people.all()


@pytest.mark.django_db
def test_swap_people_on_unowned_duty(test_duties, test_users):
    target_duty = test_duties[5]
    user1, user2 = test_users[:2]

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapPeopleRequest.objects.create(
            current_user=user1, to_swap=user2, duty=target_duty
        )

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()


@pytest.mark.django_db
def test_swap_people_self(test_duties, test_users):
    target_duty = test_duties[5]
    user1 = user2 = test_users[0]

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapPeopleRequest.objects.create(
            current_user=user1, to_swap=user2, duty=target_duty
        )

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()
