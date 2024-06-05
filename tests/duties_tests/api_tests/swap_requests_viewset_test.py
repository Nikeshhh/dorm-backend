from django.urls import reverse
from rest_framework.status import HTTP_200_OK
import pytest

from core.apps.duties.models import SwapDutiesRequest, SwapPeopleRequest


@pytest.mark.django_db
def test_list(client, user_for_client, test_duties):  # TODO: implement
    """Incoming requests"""
    test_duty = test_duties[6]
    test_user = test_duty.people.first()

    duty_to_swap = test_duties[2]
    user_to_swap = duty_to_swap.people.first()

    client.force_authenticate(test_user)

    swap_people_request = SwapPeopleRequest.objects.create(
        duty=duty_to_swap, current_user=user_to_swap, to_swap=test_user
    )

    swap_duties_request = SwapDutiesRequest.objects.create(
        first_duty=duty_to_swap,
        first_user=user_to_swap,
        second_duty=test_duty,
        second_user=test_user,
    )

    url = reverse("requests-swaps-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0].get("pk") == swap_duties_request.pk
    assert response.json()[1].get("pk") == swap_people_request.pk
