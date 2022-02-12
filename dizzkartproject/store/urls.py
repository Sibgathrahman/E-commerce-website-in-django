
from os import name
from django.urls.conf import path
from . import views

urlpatterns = [
    
    path('<str:category_name>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('productAdd/', views.productAdd, name='productAdd'),
    path('productList/', views.productList, name='productList'),
    path('productEdit/<int:product_id>', views.productEdit, name='productEdit'),
    path('productDelete/<int:product_id>',  views.productDelete, name='productDelete'),
    path('productDetails/<int:product_id>', views.productDetails, name='productDetails'),
    path('', views.store, name='store'),
    path('<slug:category_slug>/', views.store, name='products_by_category'),
    

]
