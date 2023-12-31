# Generated by Django 4.2.4 on 2023-09-19 19:31

from django.db import migrations, models
import instructions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('description', models.TextField(max_length=250, verbose_name='Описание категории')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название инструкции')),
                ('content', models.TextField(verbose_name='Описание инструкции')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('file', models.FileField(null=True, upload_to=instructions.models.instruction_file_upload_path)),
            ],
            options={
                'verbose_name': 'Инструкция',
                'verbose_name_plural': 'Инструкции',
            },
        ),
    ]
