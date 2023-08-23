"""Определение пространства имен для core.models"""

from .base_model import BaseModel
from .base_item import BaseModelItem
from .seller import Seller

__all__ = ['BaseModel', 'BaseModelItem', 'Seller']

NAME = 'Package models'
