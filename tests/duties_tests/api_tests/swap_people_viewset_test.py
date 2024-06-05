from django.urls import reverse
import pytest

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from core.apps.duties.models import SwapPeopleRequest


@pytest.mark.django_db
def test_list(client, user_for_client, test_duties):
    """
    Тестирует успешное получение списка запросов, отправленных пользователем.
    """
    test_duty = test_duties[2]
    test_user = test_duty.people.first()

    client.force_authenticate(test_user)

    swap_request = SwapPeopleRequest.objects.create(
        duty=test_duty, current_user=test_user, to_swap=user_for_client
    )

    url = reverse("people-swaps-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.json()[0].get("pk") == swap_request.pk, print(response.json())


@pytest.mark.django_db
def test_create_swap_people_request(
    user_client, user_for_client, test_users, test_duties
):
    """
    Тестирует успешное создание запроса на замену.
    """
    target_duty = test_duties[0]
    user1, user2 = test_users[:2]

    data = {
        "to_swap_duty_pk": target_duty.pk,
        "to_swap_user_pk": user2.pk,
    }
    url = reverse("people-swaps-create-swap-people-request")
    response = user_client.post(url, data)

    assert response.status_code == HTTP_201_CREATED

    data = response.json()
    swap_request = SwapPeopleRequest.objects.get(pk=data.get("pk"))

    assert swap_request.current_user == user_for_client
    assert swap_request.to_swap == user2
    assert swap_request.duty == target_duty


@pytest.mark.django_db
def test_accept_swap_duties_request(
    user_client, user_for_client, test_users, test_duties
):
    """
    Тестирует успешное принятие запроса на замену.
    Проверяет состояние до и после принятия.
    """
    target_duty = test_duties[1]
    user1, user2 = user_for_client, test_users[1]

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

    swap_request = SwapPeopleRequest.objects.create(
        duty=target_duty, current_user=user2, to_swap=user1
    )

    url = reverse("people-swaps-accept-swap-people-request", args=(swap_request.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK

    target_duty.refresh_from_db()

    assert user1 in target_duty.people.all()
    assert user2 not in target_duty.people.all()

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
    Тестирует отклонение запроса на замену.
    Проверяет состояние до и после отклонения.
    """
    target_duty = test_duties[1]
    user1, user2 = user_for_client, test_users[1]

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

    swap_request = SwapPeopleRequest.objects.create(
        duty=target_duty, current_user=user2, to_swap=user1
    )

    url = reverse("people-swaps-decline-swap-people-request", args=(swap_request.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK

    target_duty.refresh_from_db()

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

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
    Тестирует отмену запроса на замену.
    Проверяет состояние до и после отмены.
    """
    target_duty = test_duties[0]
    user1, user2 = test_users[1], user_for_client

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

    swap_request = SwapPeopleRequest.objects.create(
        duty=target_duty, current_user=user2, to_swap=user1
    )

    url = reverse("people-swaps-cancel-swap-people-request", args=(swap_request.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK, print(response.json())

    target_duty.refresh_from_db()

    assert user1 not in target_duty.people.all()
    assert user2 in target_duty.people.all()

    swap_request.refresh_from_db()
    assert swap_request.is_mutable is False
    assert swap_request.accepted is False
    assert swap_request.declined is False
    assert swap_request.canceled is True


@pytest.mark.django_db
def test_get_incoming_requests(client, user_for_client, test_duties):  # TODO: implement
    """
    Тестирует успешное получение списка запросов, адресованных пользователю.
    """
    test_duty = test_duties[2]
    test_user = test_duty.people.first()

    client.force_authenticate(user_for_client)

    swap_request = SwapPeopleRequest.objects.create(
        duty=test_duty, current_user=test_user, to_swap=user_for_client
    )

    url = reverse("people-swaps-get-incoming-requests")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.json()[0].get("pk") == swap_request.pk, print(response.json())
