from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_succesfull_login(client, test_user):
    """Тестирует успешную авторизацию существующего пользователя"""
    url = reverse("authentication-login")
    login_data = {"username": "bebra", "password": "amogus"}
    response = client.post(url, data=login_data)

    assert response.status_code == HTTP_200_OK, print(response.json())
    assert response.cookies.get("sessionid").value


@pytest.mark.django_db
def test_failed_login(client, test_user):
    """Тестирует ошибку авторизации при неправильном пароле"""
    url = reverse("authentication-login")
    login_data = {"username": "bebra", "password": "asdfadsf"}
    response = client.post(url, data=login_data)

    assert response.status_code == HTTP_403_FORBIDDEN, print(response.json())


@pytest.mark.django_db
def test_logout(client, test_user):
    client.force_login(test_user)
    url = reverse("authentication-logout")
    response = client.post(url)

    assert response.status_code == HTTP_200_OK, print(response.json())
    assert not response.cookies.get("sessionid").value


@pytest.mark.django_db
def test_is_authenticated_false(client, test_user):
    url = reverse("authentication-is-authenticated")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK, print(response.json())
    assert not response.data.get("is_authenticated")


@pytest.mark.django_db
def test_is_authenticated_true(client, test_user):
    client.force_login(test_user)
    url = reverse("authentication-is-authenticated")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK, print(response.json())
    assert response.data.get("is_authenticated")
