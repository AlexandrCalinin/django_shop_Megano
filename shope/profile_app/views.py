"""Views for profile app"""

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from django.shortcuts import redirect, render
from .models import Profile

from django.views.generic import (
    UpdateView,
    View,
    TemplateView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditUserForm, EditProfileForm


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile_app/test.html'
    # form_class = EditProfileForm
    fields = ['avatar']
    context_object_name = 'form'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatar"] = self.object.avatar
        return context


def show_image_view(request):

    profile_form = EditProfileForm(instance=request.user.profile)
    context = {'profile': profile_form}

    return render(request, 'profile_app/test.html', context)


class AccountView(TemplateView):
    template_name = 'profile_app/account.html'


class ProfileAvatarView(TemplateView):
    template_name = 'profile_app/profileAvatar.html'
