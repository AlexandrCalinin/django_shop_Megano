from django.views.generic import TemplateView


class BaseView(TemplateView):
    template_name = 'core/product_supply.html'


class AboutView(TemplateView):
    template_name = 'core/about.html'
