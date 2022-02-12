from django.core.checks import messages
from django.contrib import messages
from django.forms.widgets import NullBooleanSelect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import Orders, Payment
from accounts.models import UserAddress, Account
from carts.models import CartItem, Carts
from store.models import Products
from carts.views import checkout
import uuid,json
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def order_product(request, total=0, product_qty=0,):
    if request.method == 'POST':
        order = Orders()
    

        address_id = request.POST['address_id']
        address_data = UserAddress.objects.get(id=address_id)
        # if request.POST.get('payment_method') == 'cash_on_delivery':
        #     payment_method = request.POST['payment_method']
        
        order_address = address_data.first_name + ", " + \
            address_data.street_address + "," + address_data.apartment + "," + \
            address_data.town + "," + str(address_data.postcode) + "," + \
            str(address_data.phone_number)

        email = request.user
        user_instance = Account.objects.get(email=email)
        # cart = Cart.objects.get(user=user_instance)
        cart_items = Carts.objects.filter(user=request.user).order_by('-id')

        for cart_item in cart_items:
            total += (cart_item.product.mrp * cart_item.product_qty)
            product_qty += cart_item.product_qty
        tax = (3 * total)/100
        grand_total = total + tax
        order_number = str(uuid.uuid4())

        for cart_item in cart_items:
            product = cart_item.product.id
            product_instance = Products.objects.get(id=product)

            order.user = user_instance
            order.product = product_instance
            order.address = order_address
            order.payment_method = "Cash on Delivery"
            order.total = total
            order.order_number = order_number
            order.save()

            products=Products.objects.get(id=product)
            products.stock -= cart_item.product_qty
            products.save()

        
        
        payment_method='Cash On Delivery'
        status='Successfully Ordered'
        order = Orders.objects.filter(order_number=order_number)
        data = Orders.objects.get(order_number=order_number)
        now=data.date
        address=data.address
        product_id=data.product_id
        product=Products.objects.filter(id=product_id)

        cart_items = Carts.objects.filter(user=request.user).order_by('-id')

        for cart_item in cart_items:
            total += (cart_item.product.mrp * cart_item.product_qty)
            product_qty += cart_item.product_qty
        tax = (3 * total)/100
        grand_total = total + tax
        print(total)
        context ={
            'order': order,
            'order_number': order_number,
            'payment_method':payment_method,
            'status':status,
            'date':now,
            'address':address,
            'product':product,
            'tax':tax,
            'grand_total':grand_total,
        }
        Carts.objects.filter(user=request.user).delete()
        return render(request,'products/order_success.html', context)
       
            
    
    return redirect(checkout)




def payment_details(request, total=0,product_qty=0):
    print('razor pay working here')
    body = json.loads(request.body)

    # cart = Products.objects.filter(user=request.user)
    # print(cart)

    payment= Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid='amount',
        status=body['status'],
    )
    payment.save()
    print(payment.payment_method)


    cart_items = Carts.objects.filter(user=request.user).order_by('-id')

    for cart_item in cart_items:
        total += (cart_item.product.mrp * cart_item.product_qty)
        product_qty += cart_item.product_qty
    tax = (3 * total)/100
    grand_total = total + tax
    order_number = str(uuid.uuid4())



    for cart_item in cart_items:
            product = cart_item.product.id
            product_instance = Products.objects.get(id=product)

    order=Orders(
        user = request.user,
        product = product_instance,
        address = 'Sibgath, Kaloor,,Ernakulam,123454,1234567890',
        payment_method = 'paypal',
        total = total,
        order_number = order_number,
    )
    order.save()

    for cart_item in cart_items:
        prod=Products.objects.get(id=product)
        prod.stock -= cart_item.product_qty
        prod.save()
    
    
    


    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id,

    }


    return JsonResponse(data)



def order_complete(request, total=0, product_qty=0):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    payment_method='PayPal'
    status='Successfully Ordered'
    order = Orders.objects.filter(order_number=order_number)
    data = Orders.objects.get(order_number=order_number)
    now=data.date
    address=data.address
    product_id=data.product_id
    product=Products.objects.filter(id=product_id)

    cart_items = Carts.objects.filter(user=request.user).order_by('-id')

    for cart_item in cart_items:
        total += (cart_item.product.mrp * cart_item.product_qty)
        product_qty += cart_item.product_qty
    tax = (3 * total)/100
    grand_total = total + tax

    context ={
        'order': order,
        'order_number': order_number,
        'payment_method':payment_method,
        'status':status,
        'date':now,
        'address':address,
        'product':product,
        'tax':tax,
        'grand_total':grand_total,
    }
    Carts.objects.get(user=request.user).delete()
    return render(request,'products/order_success.html', context)

# client=razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
# def razor_test(request):
#     order_amount= 100,
#     order_currency= "INR",
#     payment_order=client.order.create(dict(amount=100, currency="INR", payment_capture=1))
#     payment_order_id=payment_order['id']
#     context={
#         'amount': 5000,
#         'api_key':RAZORPAY_API_KEY,
#         'order_id':payment_order_id
#     }
#     return render(request, 'store/checkout.html', context)