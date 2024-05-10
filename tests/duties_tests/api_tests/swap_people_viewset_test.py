from django.urls import reverse
import pytest

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from core.apps.duties.models import SwapPeopleRequest


def test_list(): ...


@pytest.mark.django_db
def test_create_swap_people_request(
    user_client, user_for_client, test_users, test_duties
):
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


@pytest.mark.django_db
def test_decline_swap_duties_request(
    user_client, user_for_client, test_users, test_duties
):
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
