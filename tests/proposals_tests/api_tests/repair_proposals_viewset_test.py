from rest_framework.status import HTTP_200_OK
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_list(user_client, test_proposals):
    """
    Тестирует получение заявок на ремонт, которые принадлежат пользователю.
    """
    url = reverse("repair-proposals-list")
    response = user_client.get(url)

    assert len(response.json()) == 3, print(response.json())


@pytest.mark.django_db
def test_accept(test_proposals, worker_client, test_worker_user):
    """
    Тестирует успешное принятие заявки работником.
    """
    target_proposal = test_proposals[1]
    assert target_proposal.status == 0
    url = reverse("repair-proposals-accept", args=(target_proposal.pk,))
    response = worker_client.post(url)

    assert response.status_code == HTTP_200_OK
    data = response.json()

    target_proposal.refresh_from_db()
    assert data.get("pk") == target_proposal.pk
    assert target_proposal.executor == test_worker_user
    assert target_proposal.status == 1


@pytest.mark.django_db
def test_close(test_proposals, worker_client, test_worker_user):
    """
    Тестирует успешное закрытие заявки работником.
    """
    target_proposal = test_proposals[1]
    assert target_proposal.status == 0
    target_proposal.accept(test_worker_user)
    assert target_proposal.status == 1

    url = reverse("repair-proposals-close", args=(target_proposal.pk,))
    response = worker_client.post(url)

    assert response.status_code == HTTP_200_OK
    data = response.json()

    target_proposal.refresh_from_db()
    assert data.get("pk") == target_proposal.pk
    assert target_proposal.executor == test_worker_user
    assert target_proposal.status == 2


@pytest.mark.django_db
def test_decline(test_proposals, worker_client, test_worker_user):
    """
    Тестирует успешный отказ от заявки работником.
    """
    target_proposal = test_proposals[1]
    assert target_proposal.status == 0
    target_proposal.accept(test_worker_user)
    assert target_proposal.status == 1

    url = reverse("repair-proposals-decline", args=(target_proposal.pk,))
    response = worker_client.post(url)

    assert response.status_code == HTTP_200_OK
    data = response.json()

    target_proposal.refresh_from_db()
    assert data.get("pk") == target_proposal.pk
    assert target_proposal.executor is None
    assert target_proposal.status == 0


@pytest.mark.django_db
def test_cancel(user_client, user_for_client, test_proposals, test_worker_user):
    """
    Тестирует успешную отмены заявки.
    """
    target_proposal = user_for_client.repair_proposals.first()

    assert target_proposal.author == user_for_client
    assert target_proposal.status == 0
    target_proposal.accept(test_worker_user)
    assert target_proposal.status == 1

    url = reverse("repair-proposals-cancel", args=(target_proposal.pk,))
    response = user_client.post(url)

    assert response.status_code == HTTP_200_OK
    data = response.json()

    target_proposal.refresh_from_db()
    assert data.get("pk") == target_proposal.pk
    # assert target_proposal.executor is None
    assert target_proposal.status == 3
