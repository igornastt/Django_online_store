from django.views.generic import ListView
from contacts.models import Contact


class ContactListView(ListView):
    """Контроллер для страницы контактов со списком контактов из БД"""

    model = Contact
