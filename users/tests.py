from django.test import TestCase
from django.urls import reverse
from catalog.models import Category, Product
from users.models import User


class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='password123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='admin@example.com', password='password123')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('password123'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='password123')


class ProductTestCase(TestCase):

    def setUp(self):
        self.client = User()
        self.category = Category.objects.create(name='Electronics', description='Electronic items')
        self.user = User.objects.create_user(email='test@example.com', password='password123')

    def test_product_creation(self):
        self.client.login(email='test@example.com', password='password123')
        url = reverse('catalog:product_create')
        data = {
            'name': 'Smartphone',
            'description': 'A new smartphone',
            'category': self.category.id,
            'price_per_unit': 300
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'Smartphone')

    def test_product_update(self):
        product = Product.objects.create(
            name='Smartphone',
            description='A new smartphone',
            category=self.category,
            price_per_unit=300,
            owner=self.user
        )
        self.client.login(email='test@example.com', password='password123')
        url = reverse('catalog:product_update', kwargs={'pk': product.pk})
        data = {
            'name': 'Updated Smartphone',
            'description': 'An updated smartphone',
            'category': self.category.id,
            'price_per_unit': 350
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Smartphone')
