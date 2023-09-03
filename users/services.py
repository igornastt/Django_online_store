from django.core.cache import cache
import config.settings
from catalog.models import Category

def get_categories():
    """функция возвращает список категорий с возможностью кеширования"""
    if config.settings.CACHE_ENABLED:
        key = 'categories'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = Category.objects.all()
            cache.set(key, cache_data)
    else:
        cache_data = Category.objects.all()
    return cache_data
