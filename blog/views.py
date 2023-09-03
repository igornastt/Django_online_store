from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(CreateView):
    """Контроллер блога для создания новой статьи"""

    model = Blog
    fields = ('title', 'description', 'creation_date', 'preview', 'is_published')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        """Формируем человекопонятный slug-name для заголовка"""

        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """Контроллер блога для просмотра списка статей"""

    model = Blog

    def get_queryset(self, *args, **kwargs):
        """Выводим в общий список только опубликованные записи"""

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset


class BlogDetailView(DetailView):
    """Контроллер блога для детального просмотра статьи"""

    model = Blog

    def get_object(self, queryset=None):
        """Создаем счетчик просмотров"""

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(UpdateView):
    """Контроллер блога для редактирования статьи"""

    model = Blog
    fields = ('title', 'description', 'creation_date', 'preview', 'is_published')

    def get_success_url(self):
        """
        Переопределение url-адреса для перенаправления
        после успешного редактирования
        """

        return reverse('blog:view', args=[self.object.pk])


class BlogDelete(DeleteView):
    """Контроллер блога для удаления статьи"""

    model = Blog
    success_url = reverse_lazy('blog:list')
