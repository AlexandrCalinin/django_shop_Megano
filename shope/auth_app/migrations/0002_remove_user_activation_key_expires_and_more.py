# Generated by Django 4.2 on 2023-08-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activation_key_expires',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_activation_key_expires',
        ),
        migrations.AddField(
            model_name='user',
            name='activation_key_set',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_activation_key_expired',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
