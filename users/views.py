from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from skypro_diplom import settings
from users.forms import UserForm, UserRegisterForm, PasswordResetConfirmForm, CustomPasswordResetForm, ProductUpdateForm
from users.models import User
from users.services.email_send_verify import send_mail_for_verify
from django.contrib.auth.views import LoginView as BaseLoginView

from django.contrib.auth import get_user
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from catalog.models import Product
from catalog.forms import ProductCreateForm


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        form.instance.owner = get_user(self.request)  # Обновленная строка
        return super().form_valid(form)


class ProfileUpdateView(generic.UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')
    template_name = 'user_form.html'

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class EmailVerify(generic.View):
    template_name = 'verify_email.html'

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('users:login')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'email_reset.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            if form.data.get('need_generate', False):
                self.object.set_passeword(
                    self.object.make_random_password(12)
                )
                self.object.save()

        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'blog/blog_list.html'

