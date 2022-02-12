from django.db import models
from store.models import Products

# Create your models here.


class ProductImages(models.Model):
    product = models.ForeignKey(Products, default=None, on_delete=models.CASCADE)
   
    image1 = models.ImageField(upload_to='photos/products')
    image2 = models.ImageField(upload_to='photos/products')
    image3 = models.ImageField(upload_to='photos/products')
    image4 = models.ImageField(upload_to='photos/products')

    def _str_(self):
        return self.product.product_name