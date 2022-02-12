
from django.urls.conf import path
from . import views

urlpatterns = [
    path('', views.adminLogin, name='adminLogin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('adminLogout/', views.adminLogout, name='adminLogout'),
    path('customer/', views.customer, name='customer'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_details/<int:order_id>',views.order_details,name='order_details'),
    
    path('payment_view',views.payment_view,name='payment_view'),
    path('add_products/',views.add_products,name='add_products'),
    # path('payment_details/', views.payment_details,name='payment_details'),
    # path('customerList/', views.customerList, name='customerList'),
    path('activeStatus/<int:status_id>', views.activeStatus, name='activeStatus'),


]
