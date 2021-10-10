from django.urls import path

from api.v1.views import PingPongApiView, WordLexemesExtractApiView

app_name = 'api'

urlpatterns = [
    path('v1/ping/', PingPongApiView.as_view(), name='ping-pong'),
    path('v1/lexemes/',
         WordLexemesExtractApiView.as_view(),
         name='word-lexemes'),
]
