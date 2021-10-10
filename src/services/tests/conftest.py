import pytest
from services.extractors import word_lexeme_extractor as _word_lexeme_extractor


@pytest.fixture
def word_lexeme_extractor():
    return _word_lexeme_extractor
