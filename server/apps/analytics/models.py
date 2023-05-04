from django.db import models


class Customer(models.Model):
    """
    Покупатель
    """

    login = models.CharField(
        verbose_name='Логин пользователя',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.login


class Deals(models.Model):
    """
    Список сделок
    """

    customer = models.ForeignKey(
        verbose_name='Покупатель',
        to='Customer',
        on_delete=models.CASCADE,
        related_name='deals',
    )

    gems = models.ForeignKey(
        verbose_name='Камень',
        to='Gems',
        on_delete=models.CASCADE,
        related_name='deals',
    )

    total = models.IntegerField(
        verbose_name='Сумма сделки',
    )  # yapf: disable

    quantity= models.IntegerField(
        verbose_name='Колличество товара',
    )  # yapf: disable

    date = models.DateTimeField(
        verbose_name='Колличество товара',
    )  # yapf: disable

    class Meta:
        ordering = ['-date']
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.customer} - {self.total}'


class Gems(models.Model):
    """
    Камень
    """

    title = models.CharField(
        verbose_name='Название камня',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'

    def __str__(self):
        return self.title
