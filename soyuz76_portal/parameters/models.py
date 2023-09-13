from django.db import models


class Regions(models.Model):
    name = models.CharField('Регион',
                            max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион работы'
        verbose_name_plural = 'Регионы работы'


class EmployeePosition(models.Model):
    name = models.CharField('Название должности',
                            max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'