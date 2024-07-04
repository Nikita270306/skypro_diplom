import json
from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()

        with open('catalog/fixtures/product.json', encoding='utf-8') as f:
            products_data = json.load(f)

        # Создание категорий и продуктов
        for product_item in products_data:
            category_id = product_item["fields"].pop("category")  # Получаем и удаляем идентификатор категории из данных продукта
            category = Category.objects.get(pk=category_id)  # Получаем объект категории по идентификатору
            product_item["fields"]["category"] = category  # Заменяем идентификатор категории объектом категории
            Product.objects.create(**product_item["fields"])