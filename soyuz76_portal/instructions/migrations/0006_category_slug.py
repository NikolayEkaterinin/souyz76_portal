# Generated by Django 4.2.4 on 2023-09-09 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0005_alter_instruction_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=0, help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор'),
            preserve_default=False,
        ),
    ]
