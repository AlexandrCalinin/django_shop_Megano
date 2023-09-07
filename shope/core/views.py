from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from auth_app.models import User


class BaseView(View):
    template_name = 'core/product_supply.html'

    def get(self, request):
        context = {
            'user_is_authenticated': request.user.is_authenticated
        }
        return render(request=request, template_name=self.template_name, context=context)


class AboutView(TemplateView):
    template_name = 'core/about.html'
