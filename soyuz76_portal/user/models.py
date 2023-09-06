from django.contrib.auth.models import AbstractUser
from django.db import models
from parameters.models import EmployeePosition, Regions
class CustomUser(AbstractUser):
    username = models.TextField('login',
                                max_length=30,
                                blank=True,
                                unique=True,
                                )
    last_name = models.TextField('Имя пользователя',
                                 max_length=50,
                                 blank=True,)
    first_name = models.TextField('Фамилия пользователя',
                                  max_length=50,
                                  blank=True,
                                  )

    birthday = models.DateField('День рождения',
                                null=True,
                                blank=True
                                )

    employee_position = models.ForeignKey(EmployeePosition,
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE,
                                          )


class Engineer(CustomUser):
    # Здесь можно не добавлять regions, так как они уже унаследованы
    region = models.ForeignKey(Regions,
                               on_delete=models.CASCADE,
                               related_name='engineer',
                               related_query_name='engineers',
                               null=False,
                               blank=True,
                               )
    class Meta:
        verbose_name = 'Инженер'
        verbose_name_plural = 'Инженеры'

class Manager(CustomUser):
    # Здесь можно настроить regions так, чтобы менеджеры могли выбирать несколько пунктов
    regions = models.ManyToManyField(Regions,
                                     blank=True,
                                     related_name='managers',
                                     related_query_name='manager',
                                     )
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
