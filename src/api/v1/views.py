from typing import Any, List, Tuple, Union
from django.http import JsonResponse
from rest_framework.views import APIView
from app.exceptions import ExtractorInvalidWordException
from services.extractors import (many_word_lexeme_extractor,
                                 one_word_lexeme_extractor)


class PingPongApiView(APIView):
    def get(self, request) -> JsonResponse:
        return JsonResponse({
            'result': 'pong',
        })


class WordExtractApiView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        self.extractors = {
            'word': one_word_lexeme_extractor,
            'words': many_word_lexeme_extractor,
        }

    def get(self, request) -> JsonResponse:
        if 'word' not in request.GET and 'words' not in request.GET:
            return JsonResponse({
                'error': 'Word is empty.'
            })

        process_type = self.__get_process_type(request)
        data = self.__get_data(request.GET[process_type])
        extractor = self.__get_extractor(data)

        try:
            result = extractor.analyze(data)

            return JsonResponse({
                'result': result,
            })
        except ExtractorInvalidWordException as e:
            return JsonResponse({
                'error': str(e)
            })

    def __get_data(self, request_data: str) -> Union[str, List[str]]:
        words = request_data.split(',')
        if len(words) == 1:
            return words[0]

        return words

    def __get_process_type(self, request) -> str:
        return 'word' if 'word' in request.GET else 'words'

    def __get_extractor(self, data) -> Any:
        if isinstance(data, str):
            return self.extractors['word']

        return self.extractors['words']
