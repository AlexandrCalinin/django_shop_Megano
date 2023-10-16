from beartype import beartype
from django.db.models import QuerySet, OuterRef, Min, F, Count, Max, DateField, ExpressionWrapper, DurationField, \
    fields, DateTimeField, IntegerField, FloatField, Avg, When, Case, Q
from django.db.models.functions import Cast, Extract

from catalog_app.models import CompareProduct, CharacteristicType
from core.models import Price
from interface.compare_product_interface import ICompareProduct


from django.utils import timezone
today = timezone.now().date()


class CompareProductRepository(ICompareProduct):

    @beartype
    def get_compare_product_list(self, _session_key: str) -> QuerySet[CompareProduct]:
        """Вернуть кверисет продуктов для сравнения"""
        qs = CompareProduct.objects.filter(session_key=_session_key).prefetch_related(
            'product__category__characteristictype_set',
            'product__characteristics'
        )
        # lst = [i.product.id for i in qs]
        print([i.product.id for i in qs])
        today = Cast(timezone.now().date(), output_field=DateTimeField())
        date = F('product__price__created_at')
        duration_in_microseconds = Cast(today - date, output_field=IntegerField())
        new = qs.annotate(product_price=Min(F('product__price__price')), duration=Min(duration_in_microseconds))
        # product_seller = F('product__price__seller__name'),

        # last_price = Price.objects.filter(product__in=lst).annotate(duration=Min(duration_in_microseconds))
        # print(last_price, last_price.created_at)
        for i in new:
            print(i, i.product_price, i.duration)

        # today = Cast(timezone.now().date(), output_field=DateTimeField())
        # date = F('created_at')
        # duration_in_microseconds = Cast(today - date, output_field=IntegerField())
        min_price_subquery = Price.objects.filter(product=3).annotate(duration=Min(duration_in_microseconds))
        for i in min_price_subquery:
            print(i, i.created_at, i.duration)
        #
        # last_price = Price.objects.all().prefetch_related('product').latest('created_at')
        # print(last_price.product.pk, last_price, last_price.date)

        # print(min_price_subquery)
        # sell = CompareProduct.objects.filter(session_key=_session_key).annotate(seller_product=F('product__price__seller__name'))
        # print(sell)
        # for i in sell:
        #     print(i, i.seller_product)

        return qs

    @beartype
    def create_compare_product(self, _product_id: int, _session_key: str) -> None:
        """Создать продукт для сравнения"""
        CompareProduct.objects.create(product_id=_product_id, session_key=_session_key)

    @beartype
    def possible_compare_product(self, _product_id: int, _session_key: str) -> bool:
        """Проверить возможность сравнения"""
        char_qs = CharacteristicType.objects.filter(category__product__id=_product_id)
        qs = CompareProduct.objects.filter(session_key=_session_key, product__category__characteristictype__in=char_qs)
        if qs:
            return True
        return False
