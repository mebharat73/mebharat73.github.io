import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')  # Replace with your project name
application = get_asgi_application()


import web.routing  # Replace with your actual app's routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            web.routing.websocket_urlpatterns  # Replace with your actual app's routing
        )
    ),
})