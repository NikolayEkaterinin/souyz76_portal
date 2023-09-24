from django.db import models
from user.models import CustomUser
from django.contrib.auth.models import User  # Измените на вашу модель пользователей
from django.utils.text import slugify
class Post(models.Model):

    author = models.TextField(max_length=30,
                              verbose_name='Автор')
    name = models.CharField(max_length=40,
                            verbose_name='Название поста')
    description = models.TextField(max_length=300,
                                   verbose_name='Описание поста',
                                   null=True,
                                   blank=True)
    url = models.URLField(null=True,
                          verbose_name='Ссылка на инструкцию',
                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.name


class File(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             default=None
                             )
    file_name = models.CharField(max_length=255, blank=True)

    def upload_path(instance, filename):
        # Здесь instance - это экземпляр модели File, а filename - имя загружаемого файла
        return f'{instance.user.engineer_folder_path}/{filename}'

    default_file_name = lambda instance: f'файл от {instance.user.username}'
    file = models.FileField(upload_to=upload_path,
                            default=f'файл от {default_file_name}'
                            )
    upload_date = models.DateTimeField(auto_now_add=True)
