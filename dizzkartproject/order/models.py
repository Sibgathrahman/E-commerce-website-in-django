from django.db import models
from accounts.models import Account
from store.models import Products

# Create your models here.




class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.payment_id




class Orders(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=2500, null=False)
    payment_method = models.CharField(max_length=250)
    total = models.PositiveIntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=250)
    status = models.CharField(max_length=15, default='new')