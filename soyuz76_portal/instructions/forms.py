from django import forms
from .models import Category, Instruction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug']


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['title', 'content', 'category', 'author', 'file']
