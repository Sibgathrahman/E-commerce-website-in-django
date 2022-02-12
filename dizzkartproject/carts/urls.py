from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('checkout/', views.checkout, name="checkout"),

    path('buy_now/',views.buy_now, name='buy_now'),

    path('cart_increment/', views.cart_increment, name='cart_increment'),
    path('cart_decrement/', views.cart_decrement, name='cart_decrement'),
    path('input_cart/', views.input_cart, name='input_cart'),

    path('add_To_Cart/', views.add_To_Cart, name='add_To_Cart'),
    path('update_cart',views.update_cart,name='update_cart'),
    path('delete_cart_item',views.delete_cart_item,name='delete_cart_item'),

    path('add_address/', views.add_address, name='add_address'),
    path('editAddress/<int:address_id>', views.editAddress, name='editAddress'),
    # path('poduct_increment', views.poduct_increment, name='poduct_increment'),
    # path('poduct_decrement', views.poduct_decrement, name='poduct_decrement'),
]