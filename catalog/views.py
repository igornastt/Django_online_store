from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
    """Контроллер для главной страницы со списком товаров"""

    model = Product

    def get_context_data(self, **kwargs):
        """Выводим в общий список информацию об активных версиях продукта"""

        context = super().get_context_data(**kwargs)

        for product in context['object_list']:
            active_version = product.version_set.filter(is_current_version=True).first()
            if active_version:
                product.active_version_number = active_version.version_number
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None

        return context

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         name=self.kwargs.get('pk'),
    #         owner=self.request.user
    #     )


class ProductDetailView(DetailView):
    """Контроллер для страницы с описанием товара"""

    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания нового товара"""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования товара"""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('catalog:update_product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDelete(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления продукта"""

    model = Product
    success_url = reverse_lazy('catalog:list')
