from django.urls import reverse
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
