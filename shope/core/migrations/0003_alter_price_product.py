# Generated by Django 4.2 on 2023-09-26 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog_app', '0003_productviewed'),
        ('core', '0002_price_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='catalog_app.product', verbose_name='product'),
        ),
    ]