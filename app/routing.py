from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    #re_path(r"ws/app/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/app/translate/$", consumers.TranslatorConsumer.as_asgi()),
    #re_path(r"ws/app/ner/$", consumers.NerConsumer.as_asgi()),
]
