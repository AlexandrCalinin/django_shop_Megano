# Generated by Django 4.2 on 2023-09-12 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog_app', '0003_rename_chatacteristicproduct_characteristicproduct_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='characteristicproduct',
            options={'verbose_name': 'value of characteristic', 'verbose_name_plural': 'values of characteristic'},
        ),
        migrations.RemoveField(
            model_name='characteristicproduct',
            name='characteristic_type',
        ),

    ]
