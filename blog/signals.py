from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Blog


@receiver(post_save, sender=Blog)
def check_views(sender, instance, **kwargs):
    """Функция сигнал, которая слушает изменения в модели Blog"""

    if instance.views_count >= 100 and not instance.is_congratulated:
        send_mail(
            'Поздравление с достижением 100 просмотров',
            f'Поздравляю с успехом!\n'
            f'Твоя статья "{instance.title}" достигла 100 просмотров!',
            'Dm1tr1y11@yandex.ru',
            ['582620@gmail.com'],
            fail_silently=False,
        )
        instance.is_congratulated = True
        instance.save()
