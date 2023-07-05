from collections import namedtuple

from django.db import models

from users.models import User
from products.models import Basket

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

    def update_after_payment(self):
        basket = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [item.save_to_history() for item in basket],
            'total_sum': float(basket.total_sum())
        }
        basket.delete()
        self.save()
