from django import forms
from .models import Post, File


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description', 'url']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file']

