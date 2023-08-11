from django.shortcuts import render
from django.views.generic import TemplateView


class AccountView(TemplateView):
    template_name = 'profile_app/account.html'


class ProfileView(TemplateView):
    template_name = 'profile_app/profile.html'


class ProfileAvatarView(TemplateView):
    template_name = 'profile_app/profileAvatar.html'
