from django.db.models.signals import post_save
from django.dispatch import receiver

from order_app.models import OrderItem


@receiver(post_save, sender=OrderItem)
def increase_number_of_sales(sender, instance, created, **kwargs):
    print(21)
    if created:
        print(77)
