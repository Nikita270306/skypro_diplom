from django.contrib import admin

from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_per_unit', 'category',)
    search_fields = ('name', 'description',)
    list_filter = ('category',)


@admin.register(Version)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('version_name', 'version_number', 'current_version')
