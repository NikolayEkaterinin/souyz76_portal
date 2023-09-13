# Generated by Django 4.2.4 on 2023-09-11 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0007_alter_instruction_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='file',
        ),
        migrations.AddField(
            model_name='instruction',
            name='file_path',
            field=models.CharField(blank=True, help_text='Укажите путь к файлу инструкции на сервере.', max_length=255, null=True, verbose_name='Путь к файлу инструкции'),
        ),
    ]
