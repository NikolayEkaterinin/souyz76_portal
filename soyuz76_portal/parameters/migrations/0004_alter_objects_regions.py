# Generated by Django 4.2.4 on 2023-09-16 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0003_alter_objects_options_alter_objects_regions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objects',
            name='regions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parameters.regions', verbose_name='Регион нахождения объекта'),
        ),
    ]