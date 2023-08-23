from django.urls import path

from contacts.views import ContactListView
from contacts.apps import ContactsConfig

app_name = ContactsConfig.name

urlpatterns = [
    path('contacts/', ContactListView.as_view(), name='contacts'),
]