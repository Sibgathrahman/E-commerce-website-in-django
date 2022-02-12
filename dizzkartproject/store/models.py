from django.db import models
from category.models import SubCategory, Category
from django.urls import reverse

# Create your models here.


class Products(models.Model):

    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField(blank=True)
    mrp = models.FloatField()
    sale_price = models.FloatField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    size = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    parent_category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    category_name=models.CharField(max_length=100,blank=True,null=True)
    parent_category_name=models.CharField(max_length=100,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category_name, self.slug])

    def __str__(self):
        return self.product_name







# from django.db import models
# from django.db.models.fields import TextField
# from category.models import Category

# Create your models here.


# class Product(models.Model):
#     product_name = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, unique=True)
#     description = models.TextField(max_length=500, blank=True)
#     price = models.IntegerField()
#     images = models.ImageField(upload_to='photos/products')
#     stock = models.IntegerField()
#     is_available = models.BooleanField(default=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.product_name