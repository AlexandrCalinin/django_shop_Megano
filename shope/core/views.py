from django.views.generic import TemplateView


class BaseView(TemplateView):
    template_name = 'core/base.html'


class AboutView(TemplateView):
    template_name = 'core/about.html'
