from typing import Any

from app.exceptions import ExtractorInvalidWordException
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView
from services.extractors import word_lexeme_extractor
from swaggers.lexemes import word_lexemes_swagger


class PingPongApiView(APIView):
    def get(self, request) -> JsonResponse:
        return JsonResponse({
            'result': 'pong',
        })


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id='lexemes-list',
        operation_description='Получение списка лексем по словам',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'words': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    title='Список слов (через запятую)',
                    items=openapi.Items(
                        type=openapi.TYPE_STRING)
                ),
            }),
        responses={
            '200': word_lexemes_swagger.success_data(),
            '400': word_lexemes_swagger.error_data(),
        },
    )
)
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
