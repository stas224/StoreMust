import stripe

from django.db import models
from django.conf import settings

from users.models import User

stripe.api_key = settings.STRIPE_SECRET


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']

        super(Product, self).save(force_insert=False, force_update=False, using=None,
                                  update_fields=None)

    def __str__(self):
        return f'Продукт {self.name} | Категория {self.category.name}'

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub'
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(item.sum() for item in self)

    def total_quantity(self):
        return sum(item.quantity for item in self)

    def stripe_products(self):
        return [
            {'price': item.product.stripe_product_price_id, 'quantity': item.quantity}
            for item in self
        ]


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.email} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def save_to_history(self):
        item_history_dict = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return item_history_dict
