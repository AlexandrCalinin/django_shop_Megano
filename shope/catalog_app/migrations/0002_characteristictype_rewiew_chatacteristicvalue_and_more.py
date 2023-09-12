# Generated by Django 4.2 on 2023-09-12 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacteristicType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='catalog_app.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Type characteristic of product',
                'verbose_name_plural': 'Types characteristic of product',
            },
        ),

        migrations.CreateModel(
            name='ChatacteristicValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('value', models.CharField(max_length=100, verbose_name='value')),
                ('characteristic_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_value', to='catalog_app.characteristictype', verbose_name='type of characteristic')),
            ],
            options={
                'verbose_name': 'Type characteristic of product',
                'verbose_name_plural': 'Types characteristic of product',
            },
        ),
        migrations.CreateModel(
            name='ChatacteristicProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('characteristic_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_product', to='catalog_app.characteristictype', verbose_name='type of characteristic')),
                ('characteristic_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_product', to='catalog_app.chatacteristicvalue', verbose_name='value of characteristic')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_product', to='catalog_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'value of product characteristic',
                'verbose_name_plural': 'values of  product characteristic',
            },
        ),
    ]
