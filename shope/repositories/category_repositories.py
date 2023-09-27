from beartype import beartype
from django.db.models import QuerySet, Min

from catalog_app.models import Category
from interface.category_interface import ICategory


class CategoryRepository(ICategory):

    def get_category_list(self) -> QuerySet[Category]:
        """Вернуть кверисет категорий"""
        return Category.objects.all()

    @beartype
    def get_min_price_of_category(self, _category_id: int) -> float:
        """Вернуть минимальную цену продукта категории"""
        min_price = Category.objects.filter(id=_category_id).aggregate(result=Min('product__price__price'))
        return round(float(min_price['result']), 2)
