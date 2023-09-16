# Generated by Django 4.2.4 on 2023-09-16 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0002_objects'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objects',
            options={'verbose_name': 'Объект', 'verbose_name_plural': 'Объекты'},
        ),
        migrations.AlterField(
            model_name='objects',
            name='regions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parameters.regions', verbose_name='Регион нахождения объекта'),
        ),
    ]
