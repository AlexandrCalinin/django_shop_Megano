from beartype import beartype
from django.utils import timezone
from django.db.models import QuerySet, OuterRef, Min, FloatField, Subquery

from catalog_app.models import CompareProduct, CharacteristicType
from core.models import Price
from interface.compare_product_interface import ICompareProduct


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
        # print([i.product.id for i in qs])
        # today = Cast(timezone.now().date(), output_field=DateTimeField())
        # date = F('product__price__created_at')
        # duration_in_microseconds = Cast(today - date, output_field=IntegerField())
        # new = qs.annotate(product_price=Min(F('product__price__price')), duration=Min(duration_in_microseconds))

        min_price_subquery = Price.objects.filter(product=OuterRef('pk')).values('product').annotate(
            min_value=Min('price')
        ).values('min_value')[:1]
        min_price_seller_subquery = Price.objects.filter(
            product=OuterRef('pk'), price=OuterRef('min_price')
        ).values('seller_id')[:1]
        queryset = qs.annotate(
            min_price=Subquery(min_price_subquery.values('min_value'), output_field=FloatField()),
            min_price_seller_id=Subquery(min_price_seller_subquery)
        ).filter(min_price__gt=0)
        for i in min_price_subquery:
            print(i, i.created_at, i.duration)

        return queryset

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
