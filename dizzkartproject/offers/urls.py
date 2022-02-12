
from django.urls import path
from . import views

urlpatterns = [
    path('',views.coupon_offer,name='coupon_offer'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('coupon_delete/<int:coupon_id>/',views.coupon_delete, name='coupon_delete'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),

    
]  
