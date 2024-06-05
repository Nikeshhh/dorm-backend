from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from datetime import date, timedelta
import pytest


@pytest.mark.django_db
def test_list(user_client, test_duties):
    """Тестирует вью для получения списка дежурств, убеждаясь, что они правильно берут промежутки дат"""
    test_duties[0].date = date.today() - timedelta(days=1)
    test_duties[0].save()
    test_duties[-1].date = date.today() + timedelta(days=29)
    test_duties[-1].save()
    url = reverse("duty-records-list")
    response = user_client.get(url)

    assert len(response.json()) == 8


@pytest.mark.django_db
def test_duties_to_swap(client, test_duties):
    """Тестирует получение дежурств, с которыми можно обменяться (все кроме переданного)"""
    test_user = test_duties[3].people.first()
    client.force_authenticate(test_user)

    url = reverse("duty-records-duties-to-swap", args=(test_duties[3].pk,))
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == len(test_duties) - 1


@pytest.mark.django_db
def test_my_duties(client, test_duties):
    test_user = test_duties[3].people.first()
    client.force_authenticate(test_user)
    url = reverse("duty-records-my-duties")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == test_user.kitchen_duties.count()


@pytest.mark.django_db
def test_nearest_duty(client, test_duties):
    test_user = test_duties[3].people.first()
    client.force_authenticate(test_user)
    url = reverse("duty-records-my-duties")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert (
        response.json()[0].get("pk")
        == test_user.kitchen_duties.order_by("-date").first().pk
    )
