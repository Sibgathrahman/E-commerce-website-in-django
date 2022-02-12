from django.db import models

# Create your models here.


class CouponOffer(models.Model):
    coupon_name=models.CharField(max_length=100)
    coupon_id=models.CharField(max_length=100, unique=True)
    offer_persantage=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
