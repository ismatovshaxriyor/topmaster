"""
JWT authentication middleware for Channels WebSocket connections.

Clients connect with the access token as a query parameter:
    ws://host/ws/notifications/?token=<access_token>

On success, scope["user"] is the authenticated User; otherwise AnonymousUser.
"""
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user_from_token(token: str):
    from django.db import close_old_connections
    from rest_framework_simplejwt.exceptions import TokenError
    from rest_framework_simplejwt.tokens import AccessToken

    from .models import User

    close_old_connections()
    try:
        access = AccessToken(token)
        return User.objects.get(id=access["user_id"], is_active=True)
    except (TokenError, KeyError, User.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = None

        query_string = scope.get("query_string", b"").decode()
        if query_string:
            token = parse_qs(query_string).get("token", [None])[0]

        if token is None:
            for name, value in scope.get("headers", []):
                if name == b"authorization":
                    parts = value.decode().split()
                    if len(parts) == 2 and parts[0].lower() == "bearer":
                        token = parts[1]
                    break

        scope["user"] = await get_user_from_token(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)
