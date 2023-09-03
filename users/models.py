from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Номер телефона", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="Страна", **NULLABLE)
    avatar = models.ImageField(upload_to="images", verbose_name="Аватар", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
