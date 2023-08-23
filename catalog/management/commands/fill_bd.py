import json
from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Product, Category


class Command(BaseCommand):
    """
    Класс реализует очистку базы данных от старых данных
    и наполнение её новыми данными из файлов json
    """

    def handle(self, *args, **options):
        # Определение путей до файлов с данными
        products_data = 'product_data.json'
        categories_data = 'category_data.json'

        # Очищаем БД для двух моделей Product и Category
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Сбрасываем автоинкремент pk для БД, чтобы он всегда начинался с 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1")

        # Загружаем данные из файла product_data.json для модели Product
        with open(products_data) as f:
            products = json.load(f)

        # Создаем экземпляр класса Product и заполняем БД
        for item in products:
            product = Product(
                name=item['fields']['name'],
                description=item['fields']['description'],
                preview=item['fields']['preview'],
                category=item['fields']['category'],
                price=item['fields']['price'],
                creation_date=item['fields']['creation_date'],
                change_date=item['fields']['change_date']
            )
            product.save()

        # Загружаем данные из файла category_data.json для модели Category
        with open(categories_data) as f:
            categories = json.load(f)

        # Создаем экземпляр класса Category и заполняем БД
        for item in categories:
            category = Category(
                name=item['fields']['name'],
                description=item['fields']['description']
            )
            category.save()

        self.stdout.write(self.style.SUCCESS('Данные в БД "Product" и "Category" загружены успешно!'))
