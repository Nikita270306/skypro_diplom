from django.db import models
from django.db.models import ForeignKey

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(verbose_name='название', max_length=255)
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='картинка', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price_per_unit = models.IntegerField(verbose_name='цена за штуку')
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='дата последнего изменения', auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='products', verbose_name='Владелец')
    is_published = models.BooleanField(default=False, verbose_name='опубликован')

    def __str__(self):
        return f'{self.name} {self.category} {self.price_per_unit}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)
        permissions = [
            ('can_change_category', 'can_change_category'),
            ('can_change_product', 'can_change_product'),
            ('can_delete_product', 'can_delete_product')
        ]


class Version(models.Model):
    version_name = models.CharField(max_length=200, verbose_name='version name')
    version_number = models.CharField(max_length=100, verbose_name='version number', default='1.0.0')
    current_version = models.CharField(max_length=100, verbose_name='version number', default='1.0.0')
    product = ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='product')

    def __str__(self):
        return f'{self.product.name} - {self.version_name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'