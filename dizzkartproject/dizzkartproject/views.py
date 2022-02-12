from django.shortcuts import render
from carts.models import Carts
from store.models import Products


def home(request):
    # counts=0
    products = Products.objects.all()
    # cart = Carts.objects.filter(user=request.user) 
    # for item in cart:
        # counts += item.product_qty
    context = {
        'products': products,
        # 'counts':counts,
    }
    return render(request, 'home.html',context)