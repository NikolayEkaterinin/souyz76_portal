from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category, Instruction
from .forms import CategoryForm, InstructionForm


# Пользовательский тест для проверки статуса superuser
def is_superuser(user):
    return user.is_superuser


# View для создания новой категории
@user_passes_test(is_superuser)
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Замените на URL вашего списка категорий
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


# View для редактирования существующей категории
@user_passes_test(is_superuser)
def category_update_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Замените на URL вашего списка категорий
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})


# View для удаления категории
@user_passes_test(is_superuser)
def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')  # Замените на URL вашего списка категорий
    return render(request, 'category_confirm_delete.html', {'category': category})


# View для создания новой инструкции
@user_passes_test(is_superuser)
def instruction_create_view(request):
    if request.method == 'POST':
        form = InstructionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instruction_list')  # Замените на URL вашего списка инструкций
    else:
        form = InstructionForm()
    return render(request, 'instruction_form.html', {'form': form})


# View для редактирования существующей инструкции
@user_passes_test(is_superuser)
def instruction_update_view(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)
    if request.method == 'POST':
        form = InstructionForm(request.POST, instance=instruction)
        if form.is_valid():
            form.save()
            return redirect('instruction_list')  # Замените на URL вашего списка инструкций
    else:
        form = InstructionForm(instance=instruction)
    return render(request, 'instruction_form.html', {'form': form})


# View для удаления инструкции
@user_passes_test(is_superuser)
def instruction_delete_view(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)
    if request.method == 'POST':
        instruction.delete()
        return redirect('instruction_list')  # Замените на URL вашего списка инструкций
    return render(request, 'instruction_confirm_delete.html', {'instruction': instruction})
