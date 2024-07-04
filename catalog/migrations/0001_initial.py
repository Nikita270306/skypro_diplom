# Generated by Django 5.0.6 on 2024-07-03 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_name', models.CharField(max_length=200, verbose_name='version name')),
                ('version_number', models.CharField(default='1.0.0', max_length=100, verbose_name='version number')),
                ('current_version', models.CharField(default='1.0.0', max_length=100, verbose_name='version number')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='картинка')),
                ('price_per_unit', models.IntegerField(verbose_name='цена за штуку')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateField(auto_now_add=True, verbose_name='дата последнего изменения')),
                ('is_published', models.BooleanField(default=False, verbose_name='опубликован')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'ordering': ('name',),
                'permissions': [('can_change_category', 'can_change_category'), ('can_change_product', 'can_change_product'), ('can_delete_product', 'can_delete_product')],
            },
        ),
    ]
