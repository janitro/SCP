from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import web.routing 


application=ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            web.routing.websocket_urlpatterns
        )
    )
})