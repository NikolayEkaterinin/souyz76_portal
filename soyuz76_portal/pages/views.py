from urllib import request

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from instructions.models import Instruction, Category
from instructions.forms import InstructionForm, CategoryForm


class IndexPagesView(ListView):
    template_name = 'base/index.html'


class InstructionDetailView(DetailView):
    model = Instruction
    template_name = 'base/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstructionForm()
        return context


class InstructionCreateView(CreateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'base/create.html'

    def form_validate(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse('pages:profile', kwargs = {'username': username})


class InstractionUpdateView(UpdateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'base/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('pages:detail', kwargs = {'pk': pk})


class InstructionDeleteView(DeleteView):
    model = Instruction
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstructionForm(instance=self.object)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse('base:profile', kwargs={'username': username})





class AboutRegistrationView(ListView):
# Попытка передавать имя и фамилию в шаблон после регистрации
    def about_user(request):
        user = request.user
        return render(request,
                      'registration/about_registration.html',
                      {'user': user})



def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request, reason=''):
    return render(request, 'pages/500.html', status=500)