import logging
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from main.models import AuthToken

logger = logging.getLogger(__name__)
User = get_user_model()


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
        except ValueError:
            logger.warning("Authorization header has invalid format")
            raise AuthenticationFailed("Неправильный формат токена")

        if prefix.lower() != "token":
            logger.warning("Authorization header has invalid prefix")
            raise AuthenticationFailed("Неправильный тип токена")

        try:
            auth_token = AuthToken.objects.get(token=token)
        except AuthToken.DoesNotExist:
            logger.warning("Invalid token attempted authentication")
            raise AuthenticationFailed("Токен недействителен")

        user, _ = User.objects.get_or_create(
            username="system",
            defaults={"is_active": True, "is_staff": False, "is_superuser": False},
        )

        logger.info("Authenticated successfully")

        return (user, None)
