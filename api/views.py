import logging
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.auth import TokenAuthentication
from core.utils.notifications import send_telegram_message
from main.models import Menu, TelegramNotification
from .serializers import MenuSerializer

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def menu_by_slug(request, slug):
    try:
        menu = Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        logger.warning(f"Меню не найдено: {slug}")
        return Response({"error": f"Меню не найдено: {slug}"}, status=404)

    serializer = MenuSerializer(menu, context={"request":request})
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_telegram_notification(request):
    message = request.data.get("message")
    from_url = request.data.get("from_url", "")

    if not message:
        logger.warning("Текст сообщения обязателен")
        return Response({"error": "Текст сообщения обязателен"}, status=404)

    obj = TelegramNotification.objects.create(message=message, from_url=from_url)

    try:
        text = (
            f"📊 Заявка №{obj.pk}:\n"
            f"Сообщение: {obj.message}\n"
            f"Отправлено со страницы: {from_url}"
        )
        send_telegram_message(text)
        obj.is_sent = True
        obj.save(update_fields=["is_sent"])
    except Exception:
        logger.warning("Отправка уведомления в telegram не удалась")
        pass
    return Response(status=200)
