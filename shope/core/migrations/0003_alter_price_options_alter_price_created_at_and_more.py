# Generated by Django 4.2 on 2023-09-11 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog_app', '0002_alter_banner_options_alter_cartsale_options_and_more'),
        ('core', '0002_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['id'], 'verbose_name': 'price', 'verbose_name_plural': 'prices'},
        ),
        migrations.AlterField(
            model_name='price',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation time'),
        ),
        migrations.AlterField(
            model_name='price',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name="product's price"),
        ),
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='price',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_seller', to='core.seller', verbose_name='seller'),
        ),
        migrations.AlterField(
            model_name='price',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation time'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time'),
        ),
    ]
