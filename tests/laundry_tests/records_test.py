from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_records_list(user_client, test_laundry_records):
    """
    Тестирует получение всех записей.
    """
    url = reverse("laundry_records-list")
    response = user_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == len(test_laundry_records)


@pytest.mark.django_db
def test_reserve_record_success(user_client, test_laundry_records):
    """
    Тестирует успешное резервирование записи пользователем.
    Проверяет состояние записи после резервирования.
    """
    record_to_test = test_laundry_records[3]

    url = reverse("laundry_records-take-record", args=(record_to_test.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK
    record_to_test.refresh_from_db()
    assert record_to_test.is_available is False


@pytest.mark.django_db
def test_reserve_record_error(user_client, test_user, test_laundry_records):
    """
    Тестирует случай, когда пользователь пытается зарезервировать запис, которая уже занята.
    Это вызывает ошибку с кодом :400:
    """
    record_to_test = test_laundry_records[3]
    record_to_test.owner = test_user
    record_to_test.save()

    url = reverse("laundry_records-take-record", args=(record_to_test.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Запись уже занята"


@pytest.mark.django_db
def test_today_records_list(user_client, test_laundry_records):
    """
    Тестирует получение записей на сегодня.
    """
    url = reverse("laundry_records-today-records-list")
    response = user_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 12, print(response.json())


@pytest.mark.django_db
def test_free_record_success(user_client, user_for_client, test_laundry_records):
    """
    Тестирует успешную отмену резервирования.
    """
    record_to_test = test_laundry_records[3]
    record_to_test.owner = user_for_client
    record_to_test.save()

    url = reverse("laundry_records-free-record", args=(record_to_test.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK
    record_to_test.refresh_from_db()
    assert record_to_test.owner is None


@pytest.mark.django_db
def test_free_record_error_already_free(user_client, test_laundry_records):
    """
    Тестирует ошибку при попытке отмены резервирования.
    В этом случае возвращает ответ со статусом :400:
    """
    record_to_test = test_laundry_records[3]

    url = reverse("laundry_records-free-record", args=(record_to_test.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_400_BAD_REQUEST
    record_to_test.refresh_from_db()
    assert record_to_test.owner is None


@pytest.mark.django_db
def test_free_record_error_not_owned(user_client, test_user, test_laundry_records):
    """
    Тестирует ошибку при попытке отмены резервирования на записи, которая не принадлежит пользователю.
    """
    record_to_test = test_laundry_records[3]
    record_to_test.owner = test_user
    record_to_test.save()

    url = reverse("laundry_records-free-record", args=(record_to_test.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_403_FORBIDDEN
    record_to_test.refresh_from_db()
    assert record_to_test.owner == test_user
