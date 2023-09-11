from django.db import models
from django.contrib.auth import get_user_model
import os
User = get_user_model()


def instruction_file_upload_path(instance, filename):
    # Получаем название категории, связанной с этой инструкцией
    category_name = instance.category.name

    # Убираем специальные символы и пробелы из имени файла
    filename = os.path.basename(filename)

    # Генерируем путь загрузки на основе названия категории и очищенного имени файла
    return f'instruction_files/{category_name}/{filename}'


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        verbose_name='Название категории'
    )
    description = models.TextField(
        max_length=250,
        null=False,
        verbose_name='Описание категории'
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ))

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Instruction(models.Model):
    title = models.CharField(
        max_length=100,
        null=False,
        verbose_name='Название инструкции'
    )

    content = models.TextField(
        null=False,
        verbose_name='Описание инструкции'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name='Добавлено'
    )
    file = models.FileField(
        upload_to=instruction_file_upload_path,
        null=True)

    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'

    def __str__(self):
        return self.title
