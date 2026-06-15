"""
Aggregated WebSocket URL patterns.

Each real-time app exposes `websocket_urlpatterns` in its routing module.
"""
from apps.chat.routing import websocket_urlpatterns as chat_ws
from apps.notifications.routing import websocket_urlpatterns as notif_ws

websocket_urlpatterns = [
    *chat_ws,
    *notif_ws,
]
