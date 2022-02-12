
from django.urls import path
from . import views

urlpatterns = [
    path('order_product/',views.order_product,name='order_product'),
    path('payment_details/', views.payment_details,name='payment_details'),
    path('order_complete/',views.order_complete, name='order_complete'),
    # path('razor_test',views.razor_test,name='razor_test'),

    
]  
