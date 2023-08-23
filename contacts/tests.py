from django.db import models


class Contact(models.Model):
    """Создание модели - полей контактов в таблице БД"""

    name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(max_length=100, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='телефон')
    address = models.CharField(max_length=200, verbose_name='адрес')

    def __str__(self):
        return f'{self.name}, {self.email}, {self.phone}, {self.address}'

    class Meta:
        """Представление написания заголовков в админке"""

        verbose_name = "контакт"
        verbose_name_plural = "контакты"
