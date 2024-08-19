from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_create_new_record(admin_client, admin_user, test_room):
    """
    Тестирует успешное создание новой записи в книге комнаты.
    """
    url = reverse("room_records-list")
    new_record_data = {"grade": 5, "comments": "Круто", "room_pk": test_room.pk}
    response = admin_client.post(url, new_record_data)

    assert response.status_code == HTTP_201_CREATED, print(response.json())

    assert test_room.room_records.count() == 1
    assert test_room.room_records.first().author == admin_user


@pytest.mark.django_db
def test_update_record(admin_client, admin_user, test_room_records, test_room):
    """
    Тестирует успешное редактирование записи через patch.
    """
    record_to_test = test_room_records[0]
    url = reverse("room_records-detail", args=(record_to_test.pk,))
    patch_data = {
        "grade": 5,
        "comments": "Все норм",
        # 'room_pk': test_room.pk
    }
    response = admin_client.patch(url, patch_data)

    assert response.status_code == HTTP_200_OK

    record_to_test.refresh_from_db()
    assert record_to_test.grade == patch_data["grade"]
    assert record_to_test.comments == patch_data["comments"]
    assert record_to_test.room == test_room
    assert record_to_test.author == admin_user


@pytest.mark.django_db
def test_create_new_record_validation_error(admin_client, test_room):
    """
    Тестирует ошибку при валидации оценки.
    """
    url = reverse("room_records-list")
    new_record_data = {"grade": 6, "comments": "Круто", "room_pk": test_room.pk}
    response = admin_client.post(url, new_record_data)

    assert response.status_code == HTTP_400_BAD_REQUEST, print(response.json())


@pytest.mark.django_db
def test_create_new_record_room_not_found(admin_client):
    """
    Тестирует попытку создания записи для несуществующей комнаты.
    """
    url = reverse("room_records-list")
    new_record_data = {"grade": 4, "comments": "Круто", "room_pk": 123}
    response = admin_client.post(url, new_record_data)

    assert response.status_code == HTTP_404_NOT_FOUND, print(response.json())
