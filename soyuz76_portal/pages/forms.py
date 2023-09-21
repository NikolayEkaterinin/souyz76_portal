from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description', 'url']


class FileUploadForm(forms.Form):
    file = forms.FileField()
