import uuid
from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords


class AuthToken(models.Model):
    token = models.CharField("Токен", max_length=40, unique=True, default=uuid.uuid4())
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"


class TelegramNotification(models.Model):
    message = models.CharField("Сообщение", max_length=256)
    from_url = models.CharField("Адрес отправки", max_length=256, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    is_sent = models.BooleanField("Статус отправки", default=False)

    class Meta:
        verbose_name = "Уведомление Telegram"
        verbose_name_plural = "Уведомления Telegram"

    def __str__(self):
        return f"Уведомление: {self.message}"


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=255)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    weight = models.CharField("Вес/кол-во", max_length=50, blank=True)
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return f"{self.name}: {self.weight}, {self.price}₽"


class Menu(models.Model):
	name = models.CharField("Название", max_length=255)
	slug = models.SlugField("Slug", unique=True, blank=True)
	products = models.ManyToManyField("Product", verbose_name="Блюда", related_name="menus")
	history = HistoricalRecords()

	class Meta:
		verbose_name = "Меню"
		verbose_name_plural = "Меню"

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
