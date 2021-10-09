import pytest

from app.exceptions import ExtractorInvalidWordException

pytestmark = [
    pytest.mark.django_db,
]


def test_extractor_one_word_ok(one_word_lexeme_extractor):
    got = one_word_lexeme_extractor.analyze('эротика')

    assert len(got) == 13
    assert got[0] == 'эротика'
    assert got[12] == 'эротиках'


@pytest.mark.parametrize('word', [
    None,
    '',
    dict(),
])
def test_extractor_one_word_exception(one_word_lexeme_extractor, word):
    with pytest.raises(ExtractorInvalidWordException):
        one_word_lexeme_extractor.analyze(word)
