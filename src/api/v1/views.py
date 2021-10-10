from typing import Any

from app.exceptions import ExtractorInvalidWordException
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from services.extractors import word_lexeme_extractor


class PingPongApiView(APIView):
    def get(self, request) -> JsonResponse:
        return JsonResponse({
            'result': 'pong',
        })


class WordLexemesExtractApiView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        self.extractor = word_lexeme_extractor

    def post(self, request: Request) -> JsonResponse:
        if 'words' not in request.data:
            return JsonResponse({
                'error': 'List of words is empty.'
            }, status=400)

        try:
            result = self.extractor.extract(request.data['words'])

            return JsonResponse({
                'result': result,
            })
        except ExtractorInvalidWordException as e:
            return JsonResponse({
                'error': str(e)
            }, status=400)
