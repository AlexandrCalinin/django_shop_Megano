# Generated by Django 4.2 on 2023-10-12 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog_app', '0002_alter_characteristicproduct_characteristic_value_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rewiew',
            options={'ordering': ['created_at'], 'verbose_name': 'rewiew', 'verbose_name_plural': 'reviews'},
        ),
        migrations.RemoveField(
            model_name='banner',
            name='category_min_price',
        ),
        migrations.AlterField(
            model_name='rewiew',
            name='text',
            field=models.TextField(verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='rewiew',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.CreateModel(
            name='ProductViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'viewed product',
                'verbose_name_plural': 'viewed products',
                'ordering': ['id'],
            },
        ),
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
