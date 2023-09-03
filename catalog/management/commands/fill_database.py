from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Fill the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Удаление старых данных...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Создание категории...')
        Category.objects.create(title='Фрукты', text='Сочные, свежие, спелые')
        Category.objects.create(title='Овощи', text='Прям как у бабушки с рынка')

        self.stdout.write('Создание продукта...')
        category1 = Category.objects.get(title='Фрукты')
        Product.objects.create(title='Яблоки', text='красненькие, хорошенькие, сладкие',
                               category=category1, price=100)

        category2 = Category.objects.get(title='Овощи')
        Product.objects.create(title='Помидоры', text='наливные , в салатик самое то',
                               category=category2, price=150)

        self.stdout.write(self.style.SUCCESS('База успешно заполнена!'))
