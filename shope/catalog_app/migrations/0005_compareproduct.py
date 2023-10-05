# Generated by Django 4.2 on 2023-10-05 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog_app', '0004_remove_banner_category_min_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompareProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('session_key', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='session key')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product for comparison',
                'verbose_name_plural': 'products for comparison',
                'ordering': ['id'],
            },
        ),
    ]
