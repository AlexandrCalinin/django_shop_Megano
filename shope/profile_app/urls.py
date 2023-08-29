from django.urls import path

from .views import *


urlpatterns = [

    path('account/', AccountView.as_view(), name='account'), # <int:profile_id>/
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profileAvatar/', ProfileAvatarView.as_view(), name='avatar'),

]
