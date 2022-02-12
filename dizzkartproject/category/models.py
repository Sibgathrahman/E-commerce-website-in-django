from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descrption = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    descrption = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    def __str__(self):
        return self.sub_category_name








# from django.db import models

# Create your models here.

# class Category(models.Model):
#     category_name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     description = models.TextField(max_length=255, blank=True)
#     cat_image = models.ImageField(upload_to='photos/categories', blank = True)


#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'




#     def __str__(self):
#         return self.category_name