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
    regions = models.ManyToManyField(Regions,
                                     blank=True,
                                     )

    engineer_folder_path = models.CharField(max_length=255,
                                            blank=True,
                                            null=True)

    is_active = models.BooleanField(default=False,
                                    verbose_name='Активирован')
