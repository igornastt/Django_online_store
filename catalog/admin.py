from django.contrib import admin
from catalog.models import Product, Category, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Представление раздела - продуктов в админке"""

    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Представление раздела - категорий в админке"""

    list_display = ('id', 'name')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """Представление раздела - версии в админке"""

    list_display = ('product', 'version_number', 'version_name', 'is_current_version')
    list_filter = ('product',)
    search_fields = ('version_number', 'version_name',)
