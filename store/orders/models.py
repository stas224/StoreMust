from collections import namedtuple

from django.db import models

from users.models import User


class Order(models.Model):
    status = namedtuple('Status', ['code', 'name'])
    CREATED, PAID, ON_WAY, DELIVERED = 0, 1, 2, 3
    STATUS = (
        status(CREATED, 'Создан'),
        status(PAID, 'Оплачен'),
        status(ON_WAY, 'В пути'),
        status(DELIVERED, 'Доставлен')
    )

    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)

    created = models.DateTimeField(auto_now_add=True)
    basket_history = models.JSONField(default=dict)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS)

    def __str__(self):
        return f'{self.id}, {self.last_name}, {self.first_name}'
