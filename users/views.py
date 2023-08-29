import random
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.forms import UserCreationForm, UserProfileForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from users.models import User


class RegisterView(CreateView):
    """Контроллер для страницы контактов со списком контактов из БД"""

    model = User
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

    def form_valid(self, form):
        new_user = form.save()
        token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = '127.0.0.1:8000'
        send_mail(
            subject='Поздравляем с регистрацией',
            message=f"Подтвердите свой адрес электронной почты. Перейдите по ссылке: http://{current_site}{activation_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

class UserConfirmationSentView(PasswordResetDoneView):
    """Успешный первый этап регистрации"""
    template_name = "users/registration/registration_sent_done.html"


class UserConfirmEmailView(View):
    """Пользователь подтверждает свою регистрацию"""
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class UserConfirmedView(TemplateView):
    """Регистрация пользователя завершена, вывод информации об этом"""
    template_name = 'users/registration/registration_confirmed.html'
    title = "Your email is activated."


class UserUpdateView(UpdateView):
    """Профиль пользователя """
    model = User
    success_url = reverse_lazy("users:profile")
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        return self.request.user


def generate_password(request):
    """Сгенерировать новый пароль для пользователя по желанию"""
    print('я запустилась')
    new_password = "".join([str(random.randint(0, 9)) for _ in range(12)])
    print('я сгенирировала пароль')
    send_mail(request.user.email, "Changed password on site", new_password)
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse("index"))

def password_reset(request):
    """Сгенерировать новый пароль для пользователя если пароль забыли"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = "".join([str(random.randint(0, 9)) for _ in range(12)])
            user.set_password(new_password)
            user.save()

            subject = "Changed password on site"
            message = f"Your new password: {new_password}"
            send_mail(user.email, subject, message)

            return redirect(reverse("users:login"))  # Перенаправление на страницу входа
        except User.DoesNotExist:
            return render(request, 'users/registration/password_reset_form.html', {'error_message': 'User not found'})  # Отображение формы с сообщением об ошибке
    return render(request, 'users/registration/password_reset_form.html')  # Вывод формы для ввода email
