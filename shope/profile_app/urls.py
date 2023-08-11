from django.urls import path

from .views import *


urlpatterns = [

    path('account/', AccountView.as_view(), name='account'), # 'account/<str:slug>/'
    path('profile/', ProfileView.as_view(), name='profile'), # 'profile/<str:slug>/'
    path('profileAvatar/', ProfileAvatarView.as_view(), name='avatar'), # 'profileAvatar/<str:slug>/'

]
