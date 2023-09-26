from django.db.models import QuerySet, Min
import random

from catalog_app.models import Banner, Category
from interface.banner_interface import IBanner


class BannerRepository(IBanner):

    def get_banner_list(self, const: int) -> QuerySet[Banner]:
        """Вернуть кверисет слайдеров"""
        qs = Banner.objects.filter(is_active=True).select_related('category')
        if len(qs) > const:
            const_num_list = random.sample([banner.category.pk for banner in qs], const)
            qs = qs.filter(category__id__in=const_num_list)
        for banner in qs:
            min_price = Category.objects.filter(id=banner.category.pk).aggregate(result=Min('product__price__price'))
            banner.category_min_price = round(float(min_price['result']), 2)
            banner.save()
        return qs
