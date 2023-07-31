from django.shortcuts import render


def base_template_view(request):
    """
    Вьюшка для проверки базового шаблона
    """
    return render(request, 'core/base.html')
