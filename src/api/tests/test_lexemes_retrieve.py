import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_lexemes_retrieve_ok(auth_api):
    got = auth_api.post('/api/v1/lexemes/', expected_status_code=200, data={
        'words': [
            "секс",
            "скачать",
            "картинка",
        ],
    })

    assert 'result' in got
    assert len(got['result'].keys()) == 3
    assert len(got['result']['секс']) == 12
    assert len(got['result']['скачать']) == 75
    assert len(got['result']['картинка']) == 13


@pytest.mark.parametrize('data, error', [
    ['', 'List of words is empty.'],
    [{}, 'List of words is empty.'],
    [{'words': ''}, 'List of words is empty.'],
    [{'words': None}, 'List of words is empty.'],
    [{'words': []}, 'List of words is empty.'],
    [{'words': ['вот', {}, 'тест']}, 'List of words has invalid element.'],
    [{'words': ['', '']}, 'List of words has empty element.'],
])
def test_lexemes_retrieve_exception(auth_api, data, error):
    got = auth_api.post('/api/v1/lexemes/',
                        expected_status_code=400,
                        data=data)

    assert 'error' in got
    assert got['error'] == error
