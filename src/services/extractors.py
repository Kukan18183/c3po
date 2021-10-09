from typing import Dict, List

import pymorphy2
from app.exceptions import ExtractorInvalidWordException


class ManyWordLexemeExtractor():
    def __init__(self) -> None:
        self.analyzer = pymorphy2.MorphAnalyzer()

    def analyze(self, words: List[str]) -> Dict[str, List[str]]:
        self.__check(words)
        return self.__process(words)

    def __process(self, words: List[str]) -> Dict[str, List[str]]:
        return {x: self.__process_one(x) for x in words}

    def __process_one(self, word: str) -> List[str]:
        data = self.analyzer.parse(word)[0]

        return [x.word for x in data.lexeme]

    def __check(self, words: List[str]) -> None:
        if words is None or not len(words):
            raise ExtractorInvalidWordException('List of words is empty.')

        if not isinstance(words, list):
            raise ExtractorInvalidWordException(
                'List of words has invalid type.'
            )

        if all([x == '' for x in words]):
            raise ExtractorInvalidWordException(
                'List of words has empty element.'
            )

        if not all([isinstance(x, str) for x in words]):
            raise ExtractorInvalidWordException(
                'List of words has invalid element.'
            )

        return None


class OneWordLexemeExtractor():
    def __init__(self) -> None:
        self.analyzer = pymorphy2.MorphAnalyzer()

    def analyze(self, word: str) -> List[str]:
        self.__check(word)

        return self.__process(word)

    def __process(self, word: str) -> List[str]:
        data = self.analyzer.parse(word)[0]
        return [x.word for x in data.lexeme]

    def __check(self, word: str) -> None:
        if not word:
            raise ExtractorInvalidWordException('Word is empty.')

        if not isinstance(word, str):
            raise ExtractorInvalidWordException('Word is not str.')

        return None


one_word_lexeme_extractor = OneWordLexemeExtractor()
many_word_lexeme_extractor = ManyWordLexemeExtractor()
