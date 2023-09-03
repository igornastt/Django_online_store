from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания суперюзера"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@sky.pro",
            first_name="admin",
            last_name="admin",
            is_superuser=True,
            is_staff=True,
            is_active=True
            )

        user.set_password("1005")
        user.save()
