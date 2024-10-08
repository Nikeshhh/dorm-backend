import pytest

from core.apps.duties.exceptions import DutySwapException
from core.apps.duties.services import SwapPeopleService


@pytest.mark.django_db
def test_swap_people_accept_success(test_duties, test_users):
    """
    Тестирует принятие запроса на замену.
    Проверяет состояние до и после принятия.
    """
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    swap_request = SwapPeopleService.create(
        initiator=user1, target=user2, initiator_duty=target_duty
    )

    swap_people_service = SwapPeopleService(user2, swap_request)

    swap_people_service.accept()

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is True
    assert swap_request.declined is False
    assert swap_request.canceled is False


@pytest.mark.django_db
def test_swap_people_decline_success(test_duties, test_users):
    """
    Тестирует отклонение запроса на замену.
    Проверяет состояние до и после отклонения.
    """
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    swap_request = SwapPeopleService.create(
        initiator=user1, target=user2, initiator_duty=target_duty
    )

    swap_people_service = SwapPeopleService(user2, swap_request)

    swap_people_service.decline()

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is False
    assert swap_request.declined is True
    assert swap_request.canceled is False


@pytest.mark.django_db
def test_swap_people_on_already_in_duty(test_duties, test_users):
    """
    Пользователь пытается заменить себя на человека, который уже присутствует в этом дежурстве.
    Это вызывает ошибку :DutySwapException:
    """
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]
    target_duty.people.add(user2)

    assert user1 in target_duty.people.all()
    assert user2 in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapPeopleService.create(
            initiator=user1, target=user2, initiator_duty=target_duty
        )

    assert user1 in target_duty.people.all()
    assert user2 in target_duty.people.all()


@pytest.mark.django_db
def test_swap_people_on_unowned_duty(test_duties, test_users):
    """
    Пользователь создать запрос на замену на дежурстве, в котором его нет.
    Это вызывает ошибку :DutySwapException:
    """
    target_duty = test_duties[5]
    user1, user2 = test_users[:2]

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapPeopleService.create(
            initiator=user1, target=user2, initiator_duty=target_duty
        )

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()


@pytest.mark.django_db
def test_swap_people_self(test_duties, test_users):
    """
    Пользователь пытается создать запрос на замену себя на себя.
    Это вызывает ошибку :DutySwapException:
    """
    target_duty = test_duties[5]
    user1 = user2 = test_users[0]

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()

    with pytest.raises(DutySwapException):
        SwapPeopleService.create(
            initiator=user1, target=user2, initiator_duty=target_duty
        )

    assert user1 not in target_duty.people.all()
    assert user2 not in target_duty.people.all()
