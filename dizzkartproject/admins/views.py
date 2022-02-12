from collections import Counter
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from django.contrib import messages
from order.models import Orders, Payment
from accounts.models import Account, UserAddress
from category.models import Category, SubCategory
from store.models import Products
from .models import ProductImages
from carts.models import Carts
import json, uuid

# Create your views here.

def payment_view(request):
    data=Payment.objects.all()

    return render(request, 'admin/payment.html',{'data':data})




# def payment_details(request, total=0,product_qty=0):

#     body = json.loads(request.body)

#     # cart = Products.objects.filter(user=request.user)
#     # print(cart)

#     payment= Payment(
#         user=request.user,
#         payment_id=body['transID'],
#         payment_method=body['payment_method'],
#         amount_paid='amount',
#         status=body['status'],
#     )
#     payment.save()
#     print(payment.payment_method)

#     # address_id = request.POST['address_id']
#     # address_data = UserAddress.objects.get(id=address_id)

#     # order_address = address_data.first_name + ", " + \
#     #         address_data.street_address + "," + address_data.apartment + "," + \
#     #         address_data.town + "," + str(address_data.postcode) + "," + \
#     #         str(address_data.phone_number)



#     cart_items = Carts.objects.filter(user=request.user).order_by('-id')

#     for cart_item in cart_items:
#         total += (cart_item.product.mrp * cart_item.product_qty)
#         product_qty += cart_item.product_qty
#     tax = (3 * total)/100
#     grand_total = total + tax
#     order_number = str(uuid.uuid4())



#     for cart_item in cart_items:
#             product = cart_item.product.id
#             product_instance = Products.objects.get(id=product)

#     order=Orders(
#         user = request.user,
#         product = product_instance,
#         address = 'address',
#         payment_method = 'paypal',
#         total = total,
#         order_number = order_number,
#     )
    
    
#     order.save()
#     print(order.total)
#     return render(request, 'admin/payment.html')


def admin_dashboard(request):
    pass




def adminLogin(request):
    if request.session.has_key('admin_login'):
        total=0
        revenue=Orders.objects.all()
        length_order=Orders.objects.all().count()
        users_count = Account.objects.all().count()
        total_products = Products.objects.all().count()
        
        for item in revenue:
            total += item.total

        avg_sale=total/length_order
        avg_item=length_order/12

        context = {
            'total': total,
            'length_order': length_order,
            'users_count':users_count,
            'total_products': total_products,
            'avg_sale':avg_sale,
            'avg_item':avg_item,
        }
        return render(request, 'admin/adminPanel.html', context)
    else:
        if request.method == 'POST':
            username = request.POST['admin_username']
            password = request.POST['admin_password']
            user = auth.authenticate(username=username, password=password)
            # if user is not None and user. is_superuser:
            if username=='admin' and password=='admin':
                # auth.login(request, user)
                # session created
                request.session['admin_login'] = True
                return render(request, 'admin/adminPanel.html',{'total':'12345'})
            else:
                messages.info(request, 'Invalid Credentials ',
                              extra_tags="admin_invalid_login")
                return render(request, 'admin/adminLogin.html')
        else:
            return render(request, 'admin/adminLogin.html')


def customer(request):
    data = Account.objects.all().order_by('id')
    return render(request, 'admin/customerList.html', {'data': data})




def order_list(request):
    order_details = Orders.objects.all().order_by('id')
    return render(request, 'admin/order_list.html', {'order_details': order_details})



def order_details(request, order_id):
    if request.method == 'POST':
        ordered_items = Orders.objects.get(id = order_id)
        status_update = request.POST['status_id']
        ordered_items.status = status_update
        ordered_items.save()
        return redirect(order_list)
    ordered_items = Orders.objects.get(id = order_id)
    return render(request,'admin/ordered_items.html', {'ordered_items':ordered_items})



def activeStatus(request, status_id):
    user = Account.objects.get(id=status_id)
    if user.is_active:
        user.is_active = False
        user.save()
        return redirect(customer)
    else:
        user.is_active = True
        user.save()
        return redirect(customer)


def adminLogout(request):
    del request.session['admin_login']
    auth.logout(request)
    return redirect(adminLogin)


def add_products(request, product=None):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        slug = product_name.replace(" ", "-")
        mrp = request.POST['mrp']
        sales_price = request.POST['sales_price']
        stock = request.POST['stock']
        sub_category_id = request.POST['subcategory']
        category_id = request.POST['category']
        description = request.POST['product_description']
        product_cover = request.FILES.get('product_cover')
        product_image1 = request.FILES.get('product_cover2')
        product_image2 = request.FILES.get('product_cover3')
        product_image3 = request.FILES.get('product_cover4')
        product_image4 = request.FILES.get('product_cover5')


        if Products.objects.filter(product_name=product_name).exists():
            messages.info(request, 'Product exists')
            return redirect('add_products')

        else:

            sub = SubCategory.objects.get(id=sub_category_id)
            cat =  Category.objects.get(id=category_id)
            product = Products(product_name=product_name, mrp=mrp, slug=slug, sale_price=sales_price, stock=stock, image =product_cover, category_name=sub, description=description,parent_category_name = cat)
            product.save()

            # product = Products(product_name=product_name, mrp=mrp, sale_price=sales_price, stock=stock, image =product_cover, description=description)
            # product.save()

            product_id = Products.objects.get(product_name=product_name)

            # if product_image1 != None:
            #     new_image = ProductImages(product_id=product_id, image=product_image1)
            #     new_image.save()

            # if product_image2 != None:
            #     new_image = ProductImages(product_id=product_id, image=product_image2)
            #     new_image.save()

            # if product_image3 != None:
            #     new_image = ProductImages(product_id=product_id, image=product_image3)
            #     new_image.save()

            # if product_image4 != None:
            #     new_image = ProductImages(product_id=product_id, image=product_image4)
            #     new_image.save()


            imgs = ProductImages(product=product_id, image1=product_image1,image2=product_image2,image3=product_image3,image4=product_image4)
            imgs.save()

            return redirect('add_products')

    else:
        data = Category.objects.all()
        sub_data = SubCategory.objects.all()
        contxt = {
            'data': data,
            'sub_data': sub_data
        }
        return render(request, 'products/productAdd.html', contxt)

