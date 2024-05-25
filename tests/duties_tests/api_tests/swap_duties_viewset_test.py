from django.urls import reverse
import pytest

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from core.apps.duties.models import SwapDutiesRequest


@pytest.mark.django_db
def test_list(user_client, user_for_client, test_users, test_duties):
    """
    Тестирует получение списка запросов на обмен для конкретного пользователя.
    Убеждается что пользователю приходят только входящие запросы.
    """
    user1, user2 = user_for_client, test_users[1]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    SwapDutiesRequest.objects.create(
        first_duty=duty1, first_user=user1, second_duty=duty2, second_user=user2
    )
    SwapDutiesRequest.objects.create(
        first_duty=duty2, first_user=user2, second_duty=duty1, second_user=user1
    )

    url = reverse("duty-swaps-list")
    response = user_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_create_swap_duties_request(
    user_client, user_for_client, test_users, test_duties
):
    """
    Тестирует успешное создание запроса на обмен.
    """
    user1, user2 = user_for_client, test_users[1]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    url = reverse("duty-swaps-create-swap-duties-request")
    data = {
        "initiator_duty_pk": duty1.pk,
        "to_swap_duty_pk": duty2.pk,
        "to_swap_resident_pk": user2.pk,
    }
    response = user_client.post(url, data)
    assert response.status_code == HTTP_201_CREATED

    data = response.json()
    swap_request = SwapDutiesRequest.objects.get(pk=data.get("pk"))

    assert swap_request.first_user == user_for_client
    assert swap_request.second_user == user2
    assert swap_request.first_duty == duty1
    assert swap_request.second_duty == duty2


@pytest.mark.django_db
def test_accept_swap_duties_request(
    user_client, user_for_client, test_users, test_duties
):
    """
    Тестирует успешное принятие запроса на обмен.
    Проверяет состояние до и после принятия запроса.
    """
    user1, user2 = user_for_client, test_users[1]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    assert user1 in duty1.people.all()
    assert user2 in duty2.people.all()
    assert user1 not in duty2.people.all()
    assert user2 not in duty1.people.all()

    swap_request = SwapDutiesRequest.objects.create(
        first_user=user2,
        second_user=user1,
        first_duty=duty2,
        second_duty=duty1,
    )

    url = reverse("duty-swaps-accept-swap-duties-request", args=(swap_request.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK, print(response.json())

    duty1.refresh_from_db()
    duty2.refresh_from_db()

    assert user1 not in duty1.people.all()
    assert user2 not in duty2.people.all()
    assert user1 in duty2.people.all()
    assert user2 in duty1.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is True
    assert swap_request.declined is False
    assert swap_request.canceled is False


@pytest.mark.django_db
def test_decline_swap_duties_request(
    user_client, user_for_client, test_users, test_duties
):
    """
    Тестирует успешное отклонение запроса на обмен.
    Проверяет состояние до и после отмены.
    """
    user1, user2 = user_for_client, test_users[1]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    assert user1 in duty1.people.all()
    assert user2 in duty2.people.all()
    assert user1 not in duty2.people.all()
    assert user2 not in duty1.people.all()

    swap_request = SwapDutiesRequest.objects.create(
        first_user=user2,
        second_user=user1,
        first_duty=duty2,
        second_duty=duty1,
    )

    url = reverse("duty-swaps-decline-swap-duties-request", args=(swap_request.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK, print(response.json())

    duty1.refresh_from_db()
    duty2.refresh_from_db()

    assert user1 in duty1.people.all()
    assert user2 in duty2.people.all()
    assert user1 not in duty2.people.all()
    assert user2 not in duty1.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is False
    assert swap_request.declined is True
    assert swap_request.canceled is False


@pytest.mark.django_db
def test_cancel_swap_duties_request(
    user_client, user_for_client, test_users, test_duties
):
    """
    Тестиирует успешную отмену запроса на обмен.
    Проверяет состояние до и после отмены.
    """
    user1, user2 = user_for_client, test_users[1]
    duty1, duty2 = user1.kitchen_duties.first(), user2.kitchen_duties.first()

    assert user1 in duty1.people.all()
    assert user2 in duty2.people.all()
    assert user1 not in duty2.people.all()
    assert user2 not in duty1.people.all()

    swap_request = SwapDutiesRequest.objects.create(
        first_user=user1,
        second_user=user2,
        first_duty=duty1,
        second_duty=duty2,
    )

    url = reverse("duty-swaps-cancel-swap-duties-request", args=(swap_request.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK, print(response.json())

    duty1.refresh_from_db()
    duty2.refresh_from_db()

    assert user1 in duty1.people.all()
    assert user2 in duty2.people.all()
    assert user1 not in duty2.people.all()
    assert user2 not in duty1.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is False
    assert swap_request.declined is False
    assert swap_request.canceled is True
