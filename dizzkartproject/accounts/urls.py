
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('otpLogin/', views.otpLogin, name='otpLogin'),
    path('submitOtp/', views.submitOtp, name='submitOtp'),
    path('cancel_order/<int:order_id>',views.cancel_order,name='cancel_order'),
    path('my_account/', views.my_account, name='my_account'),
    path('editprofile/<int:user_id>', views.editprofile, name='editprofile'),
    path('address_management/', views.address_management, name='address_management'),
    path('add_new_address/', views.add_new_address, name='add_new_address'),
    path('change_password/', views.change_password, name='change_password')

    # path('activate/<uidb64>/<token>/',views.activate,name='activate')
]  
