from django.urls import path

from .views import *


urlpatterns = [

    path('account/<str:slug>/', AccountView.as_view(), name='account'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('profileAvatar/<str:slug>/', ProfileAvatarView.as_view(), name='avatar'),

]
