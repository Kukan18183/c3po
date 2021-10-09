import pytest


pytestmark = [
    pytest.mark.django_db,
]


def test_api_ping(auth_api):
    got = auth_api.get('/api/v1/ping/')

    assert got['result'] == 'pong'
