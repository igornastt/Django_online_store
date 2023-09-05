from catalog.models import Category, Product
from config import settings
from django.core.cache import cache

def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()
    return category_list


def get_product_list(request):
    user = request.user
    if settings.CACHE_ENABLED:
        if user.is_staff:
            key = 'product_list'
            product_list = cache.get(key)
            if product_list is None:
                product_list = Product.objects.all()
                cache.set(key, product_list)
            else:
                product_list = Product.objects.all()
        else:
            key = 'product_list_publish'
            product_list = cache.get(key)
            if product_list is None:
                product_list = Product.objects.filter(
                    status=Product.STATUS_PUBLISH
                )
                cache.set(key, product_list)
            else:
                product_list = Product.objects.filter(
                    status=Product.STATUS_PUBLISH
                )
    else:
        if user.is_staff:
            product_list = Product.objects.all()
        else:
            product_list = Product.objects.filter(
                status=Product.STATUS_PUBLISH
            )
    return product_list
