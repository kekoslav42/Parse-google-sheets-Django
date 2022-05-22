from django.db import models


class Order(models.Model):
    """
    Модель для хранения распаршенных данных из таблицы
    """
    first_id = models.IntegerField(
        verbose_name='id', blank=False, null=False
    )
    second_id = models.IntegerField(
        verbose_name='Заказ №', blank=False, null=False
    )
    price_usd = models.FloatField(
        verbose_name='стоимость,$', blank=False, null=False
    )
    price_rub = models.FloatField(
        verbose_name='стоимость,₽', blank=False, null=False
    )
    date = models.DateField(
        verbose_name='срок поставки', blank=False, null=False
    )

    class Meta:
        ordering = ('first_id', )
