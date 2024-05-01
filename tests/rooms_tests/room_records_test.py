from rest_framework.status import HTTP_200_OK
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_list_room_records(user_client, test_room_records):
    url = reverse("room_records-list")
    response = user_client.get(url)

    assert response.status_code == HTTP_200_OK
