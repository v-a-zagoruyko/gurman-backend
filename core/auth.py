import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from main.models import AuthToken

logger = logging.getLogger(__name__)


class UserWrapper:
    def __init__(self):
        pass

    @property
    def is_authenticated(self):
        return True


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

        logger.info("Authenticated successfully")
        return (UserWrapper(), None)
