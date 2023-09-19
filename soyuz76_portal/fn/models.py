from django.db import models

from parameters.models import Regions


class FnReplacement(models.Model):
    name_object = models.CharField(max_length=30,
                                 null=True,)
    sap = models.CharField(max_length=10,
                         null=True)
    legal_entity = models.CharField(max_length=100,
                                  null=True)
    addres_object = models.TextField(max_length=200,
                                   null=True)
    nomer_pos = models.IntegerField(max_length=3,
                                  null=True)
    model_fr = models.CharField(max_length=20,
                              null=True)
    sn_fr = models.BigIntegerField(max_length=20,
                              null=True)
    sn_fn = models.BigIntegerField(max_length=40,
                              null=True)
    date_fp = models.DateField(null=True)
    replacement_date = models.DateField(null=True)
    regions = models.ForeignKey(Regions,  # Укажите модель, с которой устанавливается связь
                              on_delete=models.SET_NULL,  # Действие при удалении связанной записи
                              null=True,
                              verbose_name='Регион нахождения объекта'
                              )
    class Meta:
        verbose_name = ('График замен ФН')

    def __str__(self):
        return '__all__'

