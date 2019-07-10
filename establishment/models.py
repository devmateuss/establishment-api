from django.core.validators import MinValueValidator
from django.db import models


class Estabeblishments(models.Model):
    name = models.CharField('Nome', max_length=255, null=False)
    street = models.CharField('Rua', max_length=100, null=False)
    number = models.IntegerField('Numero', validators=[MinValueValidator(1)], null=False)
    neighborhood = models.CharField('Bairro', max_length=100, null=False)
    state = models.CharField('Estado',  max_length=100, null=False)
    city = models.CharField('Estado',  max_length=100, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    class Meta:
        verbose_name = 'Estabelecimento',
        verbose_name_plural = 'Estabelecimentos'

    def __str__(self):
        return self.name

