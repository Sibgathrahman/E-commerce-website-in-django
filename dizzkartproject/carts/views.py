from django.core.checks import messages
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from order.models import Payment, Orders
from store.models import Products
from .models import Cart, CartItem, Carts
from django.contrib.auth.decorators import login_required
from accounts.models import UserAddress, Account
from dizzkartproject.views import home
from django.views.decorators.csrf import csrf_exempt
import uuid, razorpay
from dizzkartproject.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY


# Create your views here.


def add_To_Cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Products.objects.get(id=prod_id)
            if(product_check):
                if (Carts.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "Product already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.is_available==True:
                        Carts.objects.create(user=request.user, product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status': "Product Added Successfully"})

                    else:
                        return JsonResponse({'status': "Only"+str(product_check.quantity)+"quantity available"})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': "login to continue"})
    return redirect('/')










def delete_cart_item(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Carts.objects.filter(user=request.user, product_id=prod_id)):
            cartitem=Carts.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"Deleted Successfully"})
    return redirect('/')










def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    # print('hi', request.cart_id)
    if request.user.is_authenticated:
        product = Products.objects.get(id=product_id)
        user = Account.objects.get(id = request.user.id)
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request),
                user_id = user.id
            )
    

        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user_id = user.id


            )
            cart_item.save()
        # return HttpResponse(cart_item.product)
        return redirect('cart')
    else:
        product = Products.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )

        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
        # return HttpResponse(cart_item.quantity)
        return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    product_instance = Products.objects.get(id=product_id)
    CartItem.objects.filter(product=product_instance).delete()
    return redirect('cart')




def cart(request, total=0, tax = 0, grand_total = 0, cart_items=None, product_qty=0):
    cart_count = 0
    cart = Carts.objects.filter(user=request.user)
    for item in cart:
        sub_total=(item.product.mrp * item.product_qty)
        total += (item.product.mrp * item.product_qty)
        product_qty += item.product_qty
    cart_count += product_qty
    tax = (3 * total)/100
    grand_total = total + tax
    context = {
        'total':total,
        'product_qty':product_qty,
        'cart':cart,
        'tax':tax,
        'grand_total':grand_total,
        # 'sub_total':sub_total,
        'cart_count':cart_count,
    }
    return render(request, 'store/cart.html', context)



    # try:
    #     cart = Carts.objects.get(cart_id=_cart_id(request))
    #     cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    #     for cart_item in cart_items:
    #         total += (cart_item.product.mrp * cart_item.quantity)
    #         quantity += cart_item.quantity
    #     tax = (3 * total)/100
    #     grand_total = total + tax
    # except ObjectDoesNotExist:
    #     pass
    # cart = Carts.objects.get(cart_id=_cart_id(request))
    # context = {
    #     'total':total,
    #     'quantity':quantity,
    #     'cart_items':cart_items,
    #     'tax':tax,
    #     'grand_total':grand_total,
    # }
    # return render(request, 'store/cart.html', context)







def update_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Carts.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Carts.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty=prod_qty
            cart.save()
            return JsonResponse({'status':"updated successfully"})
    return redirect('/')











def user_id(request):
    if request.user.is_authenticated:
        user = request.user
        user = Account.objects.get(username=user)
    elif request.session.session_key:
        user = request.session.session_key
    else:
        user = int(uuid.uuid4())
        request.session[user] = True
        print("session", user)
    return user





def add_address(request):
    if request.method == 'POST':
        user = request.user
        user_instance = Account.objects.get(email=user)
        first_name = request.POST['address_first_name']
        last_name = request.POST['address_last_name']
        country = request.POST['address_country']
        street_address = request.POST['address_street_address']
        apartment = request.POST['address_apartment_name']
        town = request.POST['address_town']
        postcode = request.POST['address_postcode']
        phone_number = request.POST['address_phone_number']
        email = request.POST['address_email']

        if first_name!="" and country!="" and street_address!="" and postcode !="" and phone_number!="" and email !="" and len(phone_number)==10:
            address = UserAddress(
                user=user_instance,
                first_name=first_name,
                last_name=last_name,
                country=country,
                street_address=street_address,
                apartment=apartment,
                town=town,
                postcode=postcode,
                phone_number=phone_number,
                email=email,
            )
            address.save()
            return redirect('checkout')
        else:
            if first_name=="":
                messages.error(request, 'Enter first Name')
                return redirect(add_address)
            if country=="":
                messages.error(request, 'Select your country')
                return redirect(add_address)
            if street_address=="":
                messages.error(request, 'Enter Your Adress properly')
                return redirect(add_address)
            if postcode=="":
                messages.error(request, 'Enter your post code')
                return redirect(add_address)
            if phone_number=="":
                messages.error(request, 'Enter your phone number')
                return redirect(add_address)
            if email=="":
                messages.error(request, 'Enter email address')
                return redirect(add_address)
            if len(phone_number)!=10:
                messages.error(request, 'Enter a Valid Phone Number')
                return redirect(add_address)

    else:
        return render(request, 'store/addAddress.html')


def editAddress(request, address_id):
    if request.method == 'POST':
        address = UserAddress.objects.get(id=address_id)
        if request.POST.get('address_first_name') != None:
            first_name = request.POST['address_first_name']
            address.first_name = first_name
            address.save()
        if request.POST.get('address_last_name') != None:
            last_name = request.POST['address_last_name']
            address.last_name = last_name
            address.save()
        if request.POST.get('address_country') != None:
            country = request.POST['address_country']
            address.country = country
            address.save()
        if request.POST.get('address_street_address') != None:
            street_address = request.POST['address_street_address']
            address.street_address = street_address
            address.save()
        if request.POST.get('address_apartment_name') != None:
            apartment = request.POST['address_apartment_name']
            address.apartment = apartment
            address.save()
        if request.POST.get('address_town') != None:
            town = request.POST['address_town']
            address.town = town
            address.save()
        if request.POST.get('address_postcode') != None:
            postcode = request.POST['address_postcode']
            address.postcode = postcode
            address.save()
        if request.POST.get('address_phone_number') != None:
            if len(request.POST.get('address_phone_number'))==10:
                phone_number = request.POST['address_phone_number']
                address.phone_number = phone_number
                address.save()
            else:
                messages.error(request, 'Enter a Valid Phone number')
                address = UserAddress.objects.get(id=address_id)
                context = {'address': address}
                return render(request, 'store/editAddress.html', context)
        if request.POST.get('address_email') != None:
            email = request.POST['address_email']
            address.email = email
            address.save()
        return redirect('checkout')
    else:
        address = UserAddress.objects.get(id=address_id)
        context = {'address': address}
        return render(request, 'store/editAddress.html', context)










client=razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
@login_required(login_url='login')
def checkout(request, total=0, product_qty=0, cart=None):
    try:
        cart = Carts.objects.filter(user=request.user)
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart:
            total += (item.product.mrp * item.product_qty)
            product_qty += item.product_qty
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    email = request.user
    user_instance = Account.objects.get(email=email) 
    address = UserAddress.objects.filter(user=user_instance)

    order_amount= grand_total*100
    payment_order=client.order.create(dict(amount=order_amount, currency="INR", payment_capture=1))
    payment_order_id=payment_order['id']

    user=request.user
    payment_method='RazorPay'
    status='COMPLETED'
    context = {
        'total':total,
        'product_qty':product_qty,
        'cart':cart,
        'tax':tax,
        'grand_total':grand_total,
        'address':address,
        'amount': 5000,
        'api_key':RAZORPAY_API_KEY,
        'order_id':payment_order_id,
        'user':user,
    }
    if request.method=='POST':
        pay = Payment(user=user,payment_id=payment_order_id,payment_method=payment_method,amount_paid=grand_total,status=status)
        pay.save()

        cart_items = Carts.objects.filter(user=request.user).order_by('-id')

        for cart_item in cart_items:
                product = cart_item.product.id
                product_instance = Products.objects.get(id=product)

        order=Orders(
            user = request.user,
            product = product_instance,
            address = 'Sibgath, Kaloor,,Ernakulam,123454,1234567890',
            payment_method = 'RazorPay',
            total = grand_total,
            order_number = payment_order_id,
        )
        
        
        order.save()



    




        # Carts.objects.get(user=request.user).delete()
        # return render(request, 'products/order_success.html')

    else:
        return render(request, 'store/checkout.html', context)




# @csrf_exempt
# def poduct_increment(request):
#     user_id = request.POST['user_id']
#     prd_id = request.POST['prd_id']
#     cart_item = CartItem.objects.get(user=user_id, product_id = prd_id)
#     if cart_item >1:
#         cart_item.quantity += 1
#         cart_item.save()
#         cart_item = CartItem.objects.filter(user = user_id, product_id = prd_id)
#         for i in cart_item:
#             price = i.product_id.sale_price
#             qnty = i.quantity
#             sub_total = (price * qnty)
#             i.sub_total = sub_total
#             i.save()
        
#         user_cart = CartItem.objects.filter(user = user_id)
#         cart_sub_total = 0
#         for item in user_cart:
#             cart_sub_total += item.sub_total
        
#         return JsonResponse({'cart_sub_total':cart_sub_total}, safe=False)
#     else:
#         pass


# def poduct_decrement(request):
#     user_id = request.POST['user_id']
#     prd_id = request.POST['prd_id']
#     cart_item = CartItem.objects.get(user=user_id, product_id = prd_id)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1

#         cart_item.save()
#         cart_item = CartItem.objects.filter(user= user_id, product_id = prd_id)
#         for i in cart_item:
#             price = i.product_id.sale_price
#             qnty= i.quantity
#             sub_total = (price * qnty)
#             i.subtotal = sub_total
#             i.save()

#         user_cart = CartItem.objects.filter(user = user_id)
#         cart_sub_total = 0
#         for item in user_cart:
#             cart_sub_total += item.sub_total

#         return JsonResponse({'cart_sub_total':cart_sub_total}, safe=False)
#     else:
#         pass
   

# def cart_increment(request):
#     produc_id = request.POST['product_id']
#     inst = Product.objesge()
#     cart = catis.ob
#     return JsonResponse("succc")



@csrf_exempt
def input_cart(request):
    product_id = request.POST['id']
    product = Products.objects.get(id=product_id)
    cart_input = request.POST['cart_input']

    # updating prodduct carts quantity
    if request.user.is_authenticated:
        user = request.user
        user_instance = Cart.objects.get(user=user)
        update_quantity = CartItem.objects.get(
            cart=user_instance, product=product)
        if cart_input >= 1:
            update_quantity.quantity = cart_input
            update_quantity.save()
    else:
        session_key = request.session.session_key
        session_instance = Cart.objects.get(cart_id=session_key)
        update_quantity = CartItem.objects.get(
            cart=session_instance, product=product)
        if cart_input >= 1:
            update_quantity.quantity = cart_input
            update_quantity.save()
    return JsonResponse("success", safe=False)



@csrf_exempt
def cart_increment(request):
    product_id = request.POST['id']
    product = Products.objects.get(id=product_id)

    # updating prodduct carts quantity
    if request.user.is_authenticated:
        user = request.user.id
        current_user = Account.objects.get(id = user)
        user_instance = Cart.objects.get(user=user)
        update_quantity = CartItem.objects.get(
            cart=user_instance, product = product, user = current_user)
        update_quantity.quantity += 1
        update_quantity.save()
        new_quantity = update_quantity.quantity
    else:
        session_key = request.session.session_key
        session_instance = Cart.objects.get(cart_id=session_key)
        update_quantity = CartItem.objects.get( 
            cart=session_instance, product=product)
        update_quantity.quantity += 1
        update_quantity.save()
        new_quantity = update_quantity.quantity
    print("radttt", update_quantity.product.mrp)
    sub_total = update_quantity.product.mrp * update_quantity.quantity
    return JsonResponse({'sub_total': sub_total, 'new_quantity': new_quantity})


@csrf_exempt
def cart_decrement(request):

    product_id = request.POST['id']
    product = Products.objects.get(id=product_id)

    # updating prodduct carts quantity
    if request.user.is_authenticated:
        print("authenticated")
        user = request.user
        user_instance = Cart.objects.get(user=user)
        # print("user_instance", user_instance)
        update_quantity = CartItem.objects.get(
            cart=user_instance, product=product)
        if update_quantity.quantity >= 2:
            update_quantity.quantity -= 1
            update_quantity.save()
            new_quantity = update_quantity.quantity
            # print("updated quantity : ", new_quantity)
    else:
        print("not authenticated")
        session_key = request.session.session_key
        session_instance = Cart.objects.get(cart_id=session_key)
        update_quantity = CartItem.objects.get(
            cart=session_instance, product=product)
        if update_quantity.quantity >= 2:
            update_quantity.quantity -= 1
            update_quantity.save()
            new_quantity = update_quantity.quantity
            # print("updated quantity : ", new_quantity)

    # updating prodduct carts subtotal(not necessary bcoz its already done in models.py))
    sub_total = update_quantity.product.sale_price * update_quantity.quantity
    return JsonResponse({'sub_total': sub_total, 'new_quantity': new_quantity})





# def counter(request):
#     cart_count = 0
#     cart = Carts.objects.filter(user=request.user)
#     for item in cart:
#         cart_count += item.cart_count
# product_qty += item.product_qty
    # return dict(cart_count=cart_count)



def buy_now(request,product_qty=0):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            print(prod_id)
            product_check = Products.objects.get(id=prod_id)
            print(product_check)
            if(product_check):
                if (Carts.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "Product already in Cart"})
                else:
                    prod_qty = 1
                    print(prod_qty)

                    if product_check.is_available==True:
                        # cart=Carts.objects.all()
                        cart = Carts(
                            product_qty = prod_qty,
                            product_id = prod_id,
                            user = request.user,
                        )
                        cart.save()
                        return JsonResponse({'status': "Product Added Successfully"})

                    else:
                        return JsonResponse({'status': "Only"+str(product_check.quantity)+"quantity available"})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': "login to continue"})
    
    return render('/')