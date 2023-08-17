from django.urls import path

from .views import *


urlpatterns = [

    path('account/', AccountView.as_view(), name='account'), # <int:profile_id>/
    path('profile/<int:profile_id>/', ProfileView.as_view(), name='profile'),
    path('profileAvatar/<int:profile_id>/', ProfileAvatarView.as_view(), name='avatar'),

]
