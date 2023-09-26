from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import Banner


class IBanner:

    @abstractmethod
    def get_banner_list(self, const: int) -> QuerySet[Banner]:
        """Получить кверисет баннеров"""
        pass
