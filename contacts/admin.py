from django.contrib import admin
from contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Представление раздела - контакты в админке"""

    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'address',)
