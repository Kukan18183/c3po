import pytest
from services.extractors import \
    many_word_lexeme_extractor as _many_word_lexeme_extractor
from services.extractors import \
    one_word_lexeme_extractor as _one_word_lexeme_extractor


@pytest.fixture
def one_word_lexeme_extractor():
    return _one_word_lexeme_extractor


@pytest.fixture
def many_word_lexeme_extractor():
    return _many_word_lexeme_extractor
