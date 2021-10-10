from typing import Dict, List

import pymorphy2
from app.exceptions import ExtractorInvalidWordException


class WordLexemeExtractor():
    def __init__(self) -> None:
        self.analyzer = pymorphy2.MorphAnalyzer()

    def extract(self, words: List[str]) -> Dict[str, List[str]]:
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


word_lexeme_extractor = WordLexemeExtractor()
