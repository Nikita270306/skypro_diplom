import os

from catalog.models import Product

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
django.setup()

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductTests(TestCase):
    def setUp(self):
        self.user = User()
        self.user = User.objects.create_user(username='testuser', email='test_email', password='password')
        self.product = Product.objects.create(name='Test Product', price=10.00)

    def test_toggle_activity_view(self):
        response = self.client.post(reverse('products:toggle_activity', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects to success_url
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)

    def test_product_list_view_authenticated(self):
        # Логинимся как созданный пользователь
        self.user.login(username='testuser', password='password')

        # Используем правильное имя URL для списка продуктов (products:home)
        response = self.user.get(reverse('products:home'))

        # Проверяем, что произошло перенаправление
        self.assertEqual(response.status_code, 302)

        # Проверяем адрес перенаправления
        self.assertRedirects(response, reverse('users:login') + '?next=' + reverse('products:home'))