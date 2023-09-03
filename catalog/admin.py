from django.contrib import admin
from .models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'status')
    list_filter = ('category', 'status')  # Добавляем фильтр по категории
    search_fields = ('title', 'text',)  # Поля для поиска по названию и описанию


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'is_current_version')
    list_filter = ('product',)
    search_fields = ('version_number', 'version_name',)
