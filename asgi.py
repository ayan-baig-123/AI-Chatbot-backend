import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# 'chat' ko apne app name se badal dein agar zarurat ho
import routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = ProtocolTypeRouter({
    # Standard HTTP requests ke liye
    "http": get_asgi_application(),
    
    # WebSocket requests ke liye (Chat ke liye yehi zaroori hai)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
