import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_all_forms_one_word_ok(auth_api):
    got = auth_api.get('/api/v1/all_forms/?word=секс')

    assert 'result' in got
    assert len(got['result']) == 12


def test_all_forms_many_word_ok(auth_api):
    got = auth_api.get('/api/v1/all_forms/?words=порно,скачать,картинка')

    assert 'result' in got
    assert len(got['result'].keys()) == 3
    assert len(got['result']['порно']) == 12
    assert len(got['result']['скачать']) == 75
    assert len(got['result']['картинка']) == 13


@pytest.mark.parametrize('query_string, error', [
    ['', 'Word is empty.'],
    ['?word', 'Word is empty.'],
    ['?word=', 'Word is empty.'],
    ['?words', 'Word is empty.'],
    ['?words=', 'Word is empty.'],
    ['?words=,', 'List of words has empty element.'],
])
def test_all_forms_exception(auth_api, query_string, error):
    got = auth_api.get(f'/api/v1/all_forms/{query_string}')

    assert 'error' in got
    assert got['error'] == error
