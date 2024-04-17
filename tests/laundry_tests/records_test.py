from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_records_list(user_client, test_laundry_records):
    url = reverse('laundry_records-list')
    response = user_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == len(test_laundry_records)


@pytest.mark.django_db
def test_reserve_record_success(user_client, test_laundry_records):
    record_to_test = test_laundry_records[3]
    url = reverse('laundry_records-take-record', args=(record_to_test.pk, ))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK
    record_to_test.refresh_from_db()
    assert record_to_test.is_available is False
    

@pytest.mark.django_db
def test_reserve_record_error(user_client, test_user, test_laundry_records):
    record_to_test = test_laundry_records[3]
    record_to_test.owner = test_user
    record_to_test.save()
    url = reverse('laundry_records-take-record', args=(record_to_test.pk, ))
    response = user_client.post(url)

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'Запись уже занята'


@pytest.mark.django_db
def test_today_records_list(user_client, test_laundry_records):
    url = reverse('laundry_records-today-records-list')
    response = user_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 12, print(response.json())