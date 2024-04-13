from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_succesfull_login(client, test_user):
    url = reverse('authentication-login')
    login_data = {
        'username': 'bebra',
        'password': 'amogus'
    }
    response = client.post(url, data=login_data)

    assert response.status_code == HTTP_200_OK, print(response.json())


@pytest.mark.django_db
def test_failed_login(client, test_user):
    url = reverse('authentication-login')
    login_data = {
        'username': 'bebra',
        'password': 'asdfadsf'
    }
    response = client.post(url, data=login_data)

    assert response.status_code == HTTP_403_FORBIDDEN, print(response.json())