from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Fill the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Удаление старых данных...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Создание категории...')
        Category.objects.create(title='Ноутбуки', text='Классные топовые ноутбуки')
        Category.objects.create(title='Моноблоки', text='Хорошая контрастность')

        self.stdout.write('Создание продукта...')
        category1 = Category.objects.get(title='Ноутбуки')
        Product.objects.create(title='Ноутбук HP', text='15.6-дюймовом ноутбук, все продумано для каждодневной работы',
                               category=category1, price=28 700)

        category2 = Category.objects.get(title='Моноблоки')
        Product.objects.create(title='HP ProOne 600 G4', text='диагональ экрана: 21.50 ',
                               category=category2, price=39 800)

        self.stdout.write(self.style.SUCCESS('База успешно заполнена!'))
