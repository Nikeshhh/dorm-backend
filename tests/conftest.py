from django.contrib.auth import get_user_model
import pytest


UserModel = get_user_model()


@pytest.fixture
def test_user():
    new_user = UserModel.objects.create(username='bebra')
    new_user.set_password('amogus')
    new_user.save()
    return new_user