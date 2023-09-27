import random

from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import Banner
from interface.banner_interface import IBanner


class BannerRepository(IBanner):

    def get_banner_list(self, const: int) -> QuerySet[Banner]:
        """Вернуть кверисет баннеров"""
        qs = Banner.objects.filter(is_active=True).select_related('category')
        if len(qs) > const:
            const_num_list = random.sample([banner.category.pk for banner in qs], const)
            qs = qs.filter(category__id__in=const_num_list)
        return qs

    @beartype
    def update_banner_price(self, _object: Banner, _min_price: float) -> None:
        """Обновить цену для баннера"""
        _object.category_min_price = _min_price
        _object.save()
