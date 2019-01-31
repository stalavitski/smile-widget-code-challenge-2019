from django.db import models

from products.utils import get_formatted_price


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)

    def get_total(self, date, gift_card):
        """Get total price with discount in cents"""
        total = self.price
        product_price = ProductPrice.objects.for_date(date).filter(product=self).order_by('price').first()

        if product_price:
            total = product_price.price

        if gift_card:
            total -= gift_card.amount
            total = total if total > 0 else 0

        return total


class GiftCardQuerySet(models.QuerySet):
    def for_date(self, date):
        return (self.filter(models.Q(date_end__isnull=True) | models.Q(date_end__gte=date)).filter(
            date_start__lte=date))


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(
        help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    objects = GiftCardQuerySet.as_manager()

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return get_formatted_price(self.amount)


class ProductPriceQuerySet(models.QuerySet):
    def for_date(self, date):
        return (self.filter(models.Q(date_end__isnull=True) | models.Q(date_end__gte=date)).filter(
            date_start__lte=date))


class ProductPrice(models.Model):
    name = models.CharField(max_length=25, help_text='Price period name')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    product = models.ForeignKey(Product, models.CASCADE, related_name='prices')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    objects = ProductPriceQuerySet.as_manager()

    def __str__(self):
        return '{} - {}'.format(self.name, get_formatted_price(self.price))
