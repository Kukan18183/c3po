from drf_yasg import openapi


class WordLexemesSwagger:
    def success_data(self):
        result = {
            'application/json': [{
                'result': {
                    'область': [
                        'область',
                        'области',
                        'области',
                        'область',
                        'областью',
                        'области',
                        'области',
                        'областей',
                        'областям',
                        'области',
                        'областями',
                        'областях',
                    ],
                    'печать': [
                        'печать',
                        'печати',
                        'печати',
                        'печать',
                        'печатью',
                        'печати',
                        'печати',
                        'печатей',
                        'печатям',
                        'печати',
                        'печатями',
                        'печатях',
                    ],
                },
            }]
        }

        return openapi.Response(description='Пример списка лексем',
                                examples=result)

    def error_data(self):
        result = {
            'application/json': [{
                'error': 'List of words is empty.',
            }]
        }

        return openapi.Response(description='Пример ошибок',
                                examples=result)


word_lexemes_swagger = WordLexemesSwagger()
