from django.urls import path
from .views import contacts, IndexView, ProductDetailView, ProductUpdateView, ProductCreateView, ProductDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contacts),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
