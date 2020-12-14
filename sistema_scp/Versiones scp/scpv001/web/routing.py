from django.urls import path, re_path
from web import consumers

websocket_urlpatterns=[
    path('ws/notification/<str:user_id>', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<person_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

