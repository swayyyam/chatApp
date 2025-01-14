# from django.urls import path
# from .consumer import ChatConsumer

# websocket_urlpatterns = [
#     path("" , ChatConsumer.as_asgi()) ,     
# ] 

from django.urls import re_path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>\w+)/$', ChatConsumer.as_asgi()),
]