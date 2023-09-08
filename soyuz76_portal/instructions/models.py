from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100,
                            null=False,
                            verbose_name='Название категории'
                            )
    description = models.TextField(max_length=250,
                                   null=False,
                                   verbose_name='Описание категории'
                                   )


class Instruction(models.Model):
    title = models.CharField(max_length=100,
                             null=False,
                             verbose_name='Название инструкции'
                             )

    content = models.TextField(null=False,
                               verbose_name='Описание инструкции'
                               )
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=False,
                                      verbose_name='Добавлено'
                                      )
    file = models.CharField(max_length=255,
                            null=True,
                            blank=True,
                            verbose_name='Путь к файлу'
                            )

