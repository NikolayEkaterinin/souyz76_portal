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


class Objects(models.Model):
    name = models.CharField(
        max_length=20,
        null=True,
        verbose_name='Номер объекта'
    )
    sap = models.CharField(
        max_length=4,
        null=True,
        verbose_name='SAP'
    )
    address = models.CharField(
        max_length=40,
        null=True,
        verbose_name='Адрес объекта'
    )
    regions = models.ForeignKey(
        Regions,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Регион нахождения объекта'
    )

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
