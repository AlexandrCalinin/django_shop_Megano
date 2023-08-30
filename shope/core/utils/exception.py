from django.utils.translation import gettext_lazy as _


class MaxDiscountErrorException(Exception):
    """Класс для исключений неверного значения в скидках"""

    @property
    def message(self) -> str:
        """Сообщение для исключения."""
        raise NotImplementedError(_('The value of discount is more than the maximum! Max value is 99'))

    def __str__(self) -> str:
        """Отображение по умолчанию для исключения."""
        return self.message
