from django.db import models
from django.db import transaction

class SKU(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GoodsGroup(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0.0)
    reserved = models.FloatField(default=0.0)
    sku = models.ForeignKey(SKU, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(GoodsGroup, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def reserve(self, number):
        if self.quantity >= number:
            with transaction.atomic():
                self.quantity -= number
                self.reserved += number
                self.save()
                return self
        else:
            raise ValueError('Item quantity is less than is being reserved')

    def sell(self, number):
        if self.quantity >= number:
            with transaction.atomic():
                self.quantity -= number
                self.save()
                return self
        else:
            raise ValueError('Item quantity is less than is being decreased')

    def remove_from_reserve(self, number):
        if self.reserved >= number:
            with transaction.atomic():
                self.quantity += number
                self.reserved -= number
                self.save()
                return self
        else:
            raise ValueError('Item reserved quantity is less than is being removed form reserved')

    def sell_from_reserve(self, number):
        if self.reserved >= number:
            with transaction.atomic():
                self.reserved -= number
                self.save()
                return self
        else:
            raise ValueError('Item quantity is less than is being decreased')