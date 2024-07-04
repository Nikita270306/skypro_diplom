import json
from django.core.management import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()

        category_list = []
        with open('catalog/fixtures/category.json', encoding='utf-8') as f:
            dict_categ = json.load(f)

        for category in dict_categ:
            category_list.append(Category(name=category['fields']['name'], description=category['fields']['description']))

        Category.objects.bulk_create(category_list)

