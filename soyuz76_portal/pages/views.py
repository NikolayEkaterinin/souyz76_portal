from urllib import request

from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPagesView(TemplateView):
    template_name = 'base/index.html'


class AboutRegistrationView(TemplateView):
# Попытка передавать имя и фамилию в шаблон после регистрации
    def about_user(request):
        user = request.user
        return render(request, 'registration/about_registration.html', {'user': user})



def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request, reason=''):
    return render(request, 'pages/500.html', status=500)