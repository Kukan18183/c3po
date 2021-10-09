import pytest

from app.exceptions import ExtractorInvalidWordException

pytestmark = [
    pytest.mark.django_db,
]


def test_extractor_many_word_ok(many_word_lexeme_extractor):
    got = many_word_lexeme_extractor.analyze(['картинка', 'бесплатный'])

    assert len(got.keys()) == 2
    assert 'картинка' in got.keys()
    assert 'бесплатный' in got.keys()
    assert len(got['картинка']) == 13
    assert len(got['бесплатный']) == 35


@pytest.mark.parametrize('words', [
    [],
    ['', ''],
    None,
    ['sdfsdf', dict(), 'sdfsdfsdf'],
    dict()
])
def test_extractor_many_word_exception(many_word_lexeme_extractor, words):
    with pytest.raises(ExtractorInvalidWordException):
        many_word_lexeme_extractor.analyze(words)
