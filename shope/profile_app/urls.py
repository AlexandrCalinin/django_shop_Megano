from django.urls import path

from .views import (
    EditProfileView,
    AccountView,
    show_image_view,

)


urlpatterns = [

    path('account/', AccountView.as_view(), name='account'),
    path('profile/', EditProfileView.as_view(), name='profile'),
    path('profile1/', show_image_view, name='profile1'),
    # path('profileAvatar/', ProfileAvatarView.as_view(), name='avatar'),

]
