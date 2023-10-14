from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path('', cache_page(24 * 60 * 24)(BaseView.as_view()), name='home'),
    path('about/', AboutView.as_view(), name='about'),
]
