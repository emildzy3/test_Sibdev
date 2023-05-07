from django.db import models


class Deal(models.Model):
    """
    Список сделок
    """

    username = models.CharField(
        verbose_name='Логин пользователя',
        max_length=150,
    )

    gems = models.ForeignKey(
        verbose_name='Камень',
        to='Gem',
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
        verbose_name='Дата сделки',
    )  # yapf: disable

    class Meta:
        ordering = ['-date']
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return f'{self.username} - {self.total}'


class Gem(models.Model):
    """
    Камень
    """

    title = models.CharField(
        verbose_name='Название',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'

    def __str__(self):
        return self.title
