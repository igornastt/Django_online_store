from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}  # константа для необязательного поля


class Product(models.Model):
    """Модель продукта"""
    STATUS_CREATED = 'created'
    STATUS_MODERATED = 'moderated'
    STATUS_PUBLISH = 'published'
    STATUSES = (
        (STATUS_CREATED, 'Добавлен'),
        (STATUS_MODERATED, 'На модерации'),
        (STATUS_PUBLISH, 'Опубликован'),
    )

    title = models.CharField(max_length=150, verbose_name='наименование')
    text = models.TextField(max_length=10000, verbose_name='описание')
    image = models.ImageField(verbose_name='изображение', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='категория', blank=True, null=True)
    price = models.IntegerField(verbose_name='цена', blank=True, null=True)
    date_creation = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    date_change = models.DateTimeField(verbose_name='дата изменений', auto_now=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_MODERATED, verbose_name='статус')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.title}. {self.text}'

    class Meta:
        verbose_name = 'продукт'  # Настройка для наименования одного объекта
        verbose_name_plural = 'продукты'
        ordering = ('title',)
        permissions = [
            ('set_product_status', 'Can change the status of products'),
            ('change_product_description', 'Can change product description'),
            ('change_product_category', 'Can change product category'),
        ]


class Category(models.Model):
    """Модель категории"""
    title = models.CharField(max_length=150, verbose_name='наименование')
    text = models.TextField(max_length=10000, verbose_name='описание')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.title}. {self.text}'

    class Meta:
        verbose_name = 'кетегория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'категории'
        ordering = ('title',)


class Version(models.Model):
    """Модель версии"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.CharField(max_length=100, verbose_name='номер версии')
    version_name = models.CharField(max_length=100, verbose_name='название версии')
    is_current_version = models.BooleanField(default=False, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.product}, {self.version_name}, {self.version_number}'

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"
