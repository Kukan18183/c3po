from django.urls import path

from api.v1.views import PingPongApiView, WordExtractApiView

app_name = 'api'
urlpatterns = [
    path('v1/ping/', PingPongApiView.as_view(), name='ping-pong'),
    path('v1/all_forms/', WordExtractApiView.as_view(), name='word-analyzer'),
]
