from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer as _mixer

from tests.api_client import DRFClient


@pytest.fixture(autouse=True)
def main_user(mixer):
    user_opts = {
        'is_staff': True,
        'is_superuser': True,
        'email': 'main_user@mail.ru',
    }
    user = mixer.blend(User, id=167, **user_opts)

    password = 'test_pass'
    user.set_password(password)

    user.save()

    return user


@pytest.fixture
def auth_api(main_user):
    return DRFClient(user=main_user)


@pytest.fixture
def api():
    return DRFClient()


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def connect_mock_handler():
    def _connect_mock_handler(signal, **kwargs):
        handler = MagicMock()
        signal.connect(handler, **kwargs)
        return handler

    return _connect_mock_handler
