# Generated by Django 4.2.4 on 2023-09-11 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0008_remove_instruction_file_instruction_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='file_path',
        ),
        migrations.AddField(
            model_name='instruction',
            name='file',
            field=models.FileField(null=True, upload_to='instruction_files/<django.db.models.fields.related.ForeignKey>/'),
        ),
    ]