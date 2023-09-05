from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from blog.models import Blog
from catalog.forms import ProductForm, VersionForm, ProductModerForm
from catalog.models import Product, Version

from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from catalog.services import get_product_list


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



class ProductDetailView(ListView):
    template_name = 'catalog/product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, self.template_name, {'product': product})

    def get_queryset(self):
        queryset = get_product_list(request=self.request)
        return queryset



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


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('index')
    permission_required = 'catalog.change_product'

    def test_func(self):
        print('test func')
        user = self.request.user
        product = self.get_object()
        # print(product.owner)
        if product:
        # print(f'User: {user}, Product Owner: {product.owner}')
            if product.owner == user or user.is_staff:
                return True
        return False

    def get_form_class(self):
        product = self.get_object()
        user = self.request.user
        print('get_form')

        if user.is_staff:
            return ProductModerForm

        elif product.owner == user:
            print('tut')
            return ProductForm

        return super().get_form_class()


    def handle_no_permission(self):
        print('mozhet tut')
        return redirect(reverse_lazy('index'))


    def get_object(self, queryset=None):
        print("get_obj")
        self.object = super().get_object(queryset)
        # print (f'{self.object.owner}')
        if self.object.owner == self.request.user or self.request.user.is_staff:
            print("1")
            return self.object
        else:
            print("2")
            return None



    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        print("context_data")
        if user == self.object.owner:
            VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
            if self.request.method == 'POST':
                context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
                # formset = VersionFormset(self.request.POST, instance=self.object)
            else:
                context_data['formset'] = VersionFormset(instance=self.object)

            # context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        user = self.request.user
        print("form_valid")
        if user == self.object.owner:
            # context_data = self.get_context_data()
            formset = self.get_context_data()['formset']
            self.object = form.save()


            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        return super().form_valid(form)
