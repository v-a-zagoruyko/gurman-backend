import uuid
import logging
from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from simple_history.admin import SimpleHistoryAdmin
from .models import AuthToken, TelegramNotification, Category, Product, Menu, MenuItem

logger = logging.getLogger(__name__)

admin.site.site_header = "Администрирование"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Панель управления"
admin.site.site_url = "https://ресторан-гурман.рф"


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ["token", "created_at"]
    search_fields = ["token",]
    readonly_fields = ["token", "created_at"]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if '_gen_token' in request.POST:
            auth_token = self.get_object(request, object_id)
            if auth_token:
                new_token = str(uuid.uuid4())
                auth_token.token = new_token
                auth_token.save(update_fields=["token"])
                self.message_user(request, f"Новый токен сгенерирован: {new_token}")
                logger.info(f"Token (id={auth_token.id}) was changed")
            return HttpResponseRedirect(request.path)
        return super().change_view(request, object_id, form_url, extra_context)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TelegramNotification)
class TelegramNotificationAdmin(admin.ModelAdmin):
    list_display = ["message", "from_url", "created_at", "is_sent"]
    list_filter = ["is_sent",]
    search_fields = ["message", "from_url"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ["name",]
    search_fields = ["name",]

@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ["image_preview", "name", "category", "weight"]
    list_filter = ["category",]
    search_fields = ["name",]
    fields = ["name", "category", "weight", "description", "image", "image_preview_large"]
    readonly_fields = ["image_preview_large",]

    @admin.display(description="Изображение")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 60px;"/>', obj.image.url)
        return "-"

    @admin.display(description="Изображение")
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 200px;"/>', obj.image.url)
        return "-"

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    fields = ["product", "price"]
    extra = 1
    can_delete = False

@admin.register(Menu)
class MenuAdmin(SimpleHistoryAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    inlines = [MenuItemInline,]
