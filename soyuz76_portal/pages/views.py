from datetime import timezone
from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView, TemplateView)

from .models import Post
from .forms import PostForm

from instructions.models import Instruction, Category
from instructions.forms import InstructionForm, CategoryForm
from user.models import CustomUser
from user.forms import RegistrationForm, UpdateProfileForm
from fn.views import CommonViewMixin
from django.views import generic

NUMBER_OF_INSTRUCTIONS = 10

# Функция тестирования для проверки, является ли пользователь суперпользователем
def is_superuser(user):
    return user.is_superuser



"""Views функции по работе с инструкциями"""
class IndexListView(ListView):
    model = Post
    template_name = "base/index.html"
    paging = NUMBER_OF_INSTRUCTIONS
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        return context


class InstructionDetailView(LoginRequiredMixin, DetailView):
    model = Instruction
    template_name = 'base/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstructionForm()
        return context

""" Views функции по работе с постами  """
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'base/detail_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # Убедитесь, что это имя вашей формы
    template_name = 'base/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('pages:profile', kwargs={'username': username})

    def test_func(self):
        return is_superuser(self.request.user)



class InstructionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'base/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('pages:profile', kwargs={'username': username})

    def test_func(self):
        return is_superuser(self.request.user)


class InstructionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'base/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('pages:detail', kwargs={'pk': pk})

    def test_func(self):
        return is_superuser(self.request.user)


class InstructionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Instruction
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstructionForm(instance=self.object)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('base:profile', kwargs={'username': username})

    def test_func(self):
        return is_superuser(self.request.user)

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'base/create.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('pages:profile', kwargs={'username': username})

    def test_func(self):
        return is_superuser(self.request.user)


class ProfileDetailView(ListView, CommonViewMixin):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'base/profile.html'

    paginate_by = 10

    def get_queryset(self):
        queryset = CommonViewMixin().get_queryset()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Добавляем текущего пользователя в контекст

        # Извлекаем значения полей из текущего пользователя и добавляем их в контекст
        context['user_birthday'] = self.request.user.birthday
        context['user_username'] = self.request.user.username
        context['user_employee_position'] = self.request.user.employee_position

        return context


class ProfileAdminDetailView(DetailView):
    model = CustomUser  # Замените на вашу модель
    form_class = RegistrationForm
    template_name = 'base/profile_admin.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser  # Replace with your User model
    form_class = UpdateProfileForm  # Replace with your profile form
    template_name = 'base/edit_profile.html'  # Replace with the template for editing the profile

    def get_object(self, queryset=None):
        return self.request.user  # Edit the profile for the currently logged-in user

    def get_success_url(self):
        return reverse('pages:profile', kwargs={'username': self.request.user.username})


class CategoryListView(ListView):
    model = Category
    template_name = 'base/category_list.html'
    context_object_name = 'categories'


class InstructionCategoryListView(ListView):
    model = Instruction
    template_name = "base/list_instructions.html"
    ordering = ('-created_at')

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')  # Используем правильный ключ 'category_slug'
        queryset = super().get_queryset()
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')  # Используем правильный ключ 'category_slug'
        if not category_slug:
            raise Http404("Категория не найдена")
        context['category_slug'] = category_slug
        return context


class AboutRegistrationView(ListView):
    # Определяем модель, связанную с этим представлением
    model = CustomUser

    # Метод для отображения информации о пользователе
    def about_user(self, request):
        user = request.user
        return render(request, 'registration/about_registration.html', {'user': user})


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request, reason=''):
    return render(request, 'pages/500.html', status=500)
