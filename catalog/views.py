from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from blog.models import Blog
from catalog.forms import ProductForm, VersionForm, ProductModerForm
from catalog.models import Product, Version

from django.shortcuts import get_object_or_404, redirect, render
from django.views import View


class IndexView(ListView):
    template_name = 'catalog/index.html'
    model = Product

    # def get(self, request):
    #     products = Product.objects.all()
    #     return render(request, self.template_name, {'products': products})

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Если пользователь аутентифицирован (в том числе владелец товара)
            if user.is_staff or user.is_superuser:
                # Для администраторов показываем все продукты
                queryset = super().get_queryset()

            else:
                # Для остальных аутентифицированных пользователей
                queryset = super().get_queryset().filter(
                    status=Product.STATUS_PUBLISH
                )
        else:
            # Для неаутентифицированных пользователей
            queryset = super().get_queryset().filter(
                status=Product.STATUS_PUBLISH
            )
        return queryset



class ProductDetailView(View):
    template_name = 'catalog/product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, self.template_name, {'product': product})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('index')


def contacts(request):
    """Контроллер, который отвечает за отображение контактной информации."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html')

def blog_list_view(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/list.html', {'blogs': blogs})


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')
    permission_required = 'catalog.change_product'

    def test_func(self):
        user = self.request.user
        product = self.get_object()

        if product.owner == user or user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('index'))

    # def test_func(self):
    #     product = self.get_object()
    #     user = self.request.user
    #
    #     if user.is_staff:
    #         self.form_class = ProductModerForm
    #
    #     if product.owner == user:
    #         self.form_class = ProductForm
    #
    #     return self.form_class

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.owner == self.request.user or self.request.user.is_staff:
    #         return redirect(reverse('users:login'))
    #
    #     return self.object



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
