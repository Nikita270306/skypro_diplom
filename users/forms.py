from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, SetPasswordForm, PasswordResetForm
from django import forms
from django.forms import ModelForm
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from catalog.forms import FormStyleMixin
from catalog.models import Product, Category
from users.models import User
import re


class UserForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

        def validate_password(self):
            password = self.cleaned_data.get('password1')
            # Проверка длины пароля
            if len(password) < 8:
                return False, "Пароль должен быть не менее 8 символов."

            # Проверка наличия только латинских символов
            if not re.match(r'^[a-zA-Z0-9$%&!:.]+$', password):
                return False, "Пароль должен содержать только латиницу и допустимые спецсимволы ($%&!:)."

            # Проверка наличия хотя бы одного символа верхнего регистра
            if not re.search(r'[A-Z]', password):
                return False, "Пароль должен содержать минимум 1 символ верхнего регистра."

            # Проверка наличия хотя бы одного специального символа
            if not re.search(r'[$%&!:.]', password):
                return False, "Пароль должен содержать минимум 1 спец символ ($%&!:)."

            return password

        def validate_phone(self):
            phone = self.cleaned_data.get('phone')
            # Проверка, что телефон начинается с +7 и содержит ровно 10 цифр после этого
            if re.match(r'^\+7\d{10}$', phone):
                return phone
            return False, "Телефон должен начинаться с +7, после чего должно идти 10 цифр."


class CustomPasswordResetForm(FormStyleMixin, PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=50,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User


class PasswordResetConfirmForm(FormStyleMixin, SetPasswordForm):
    class Meta:
        model = User


class ProductUpdateForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price_per_unit')
