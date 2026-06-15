"""
ASGI entrypoint — serves both HTTP (Django) and WebSocket (Channels).

WebSocket routes are authenticated with JWT via the custom
JWTAuthMiddleware (token passed as ?token=<access> query param), and
collected from each app's routing module in config.routing.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

from django.core.asgi import get_asgi_application  # noqa: E402

# Initialise Django before importing anything that touches the app registry.
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import AllowedHostsOriginValidator  # noqa: E402

from apps.accounts.ws_auth import JWTAuthMiddleware  # noqa: E402
from config.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
