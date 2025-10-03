from django.urls import path
from .views import menu_by_slug, send_telegram_notification

urlpatterns = [
    path('menu/<str:slug>/', menu_by_slug, name='menu-by-slug'),
    path('notify/', send_telegram_notification, name='send-telegram-notification'),
]
