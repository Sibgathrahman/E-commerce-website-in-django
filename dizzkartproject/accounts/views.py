from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
# from django.contrib.auth.models import auth
from django.contrib import auth
from carts.models import Cart, CartItem
from store.models import Products
from .forms import RegistrationForm
from .models import Account
from dizzkartproject.views import home
import random
from order.models import Orders
from accounts.models import UserAddress
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart, CartItem

#verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            username= form.cleaned_data['username']

            if password==confirm_password and len(password)>=5 and len(phone_number)==10 and len(username)>=5:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_number= phone_number

                user.save()
                messages.success(request, 'registration successfull')
                return redirect(register)
            else:
                if password!=confirm_password:
                    messages.error(request, 'Passwords are not matching')
                    return redirect(register)
                if len(password)<5:
                    messages.error(request, 'Password should 5 or more letters')
                    return redirect(register)
                if len(phone_number)!=10:
                    messages.error(request, 'Enter a valid Mobile Number')
                    return redirect(register)
                if len(username)<5:
                    messages.error(request, 'Enter atleast 5 letters for username')
                    return redirect(register)


    else:
        form = RegistrationForm()

    form = RegistrationForm
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            print('working here')
            # try:
            #     cart = Cart.objects.get(cart_id=_cart_id(request))
            #     is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            #     if is_cart_item_exists:
            #         cart_item = CartItem.objects.filter(cart=cart)
            #         for item in cart_item:
            #             item.user = user
            #             item.save()
            # except:
            #     pass
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect(home)
        else:
            messages.error(request, 'Enter valid login details')
            return redirect('login')
    return render(request, 'accounts/login.html')



def otpLogin(request):
    global random_otp, verified_user
    if request.method == 'POST':
        phone_number = request.POST['otp_phone_number']
        if Account.objects.filter(phone_number=phone_number).exists():
            verified_user = Account.objects.get(phone_number=phone_number)
            otp = random.randint(100000, 999999)
            random_otp = otp
            content = "Your OTP of dizzkart : "+str(random_otp)
            phone_number = '+91'+str(phone_number)
            account_sid = 'AC3399ed0804a43123ae5e2f1baeb719a5'
            auth_token = '27724c048cd64eb5ba5c9230d9b481fa'
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                    body=content,
                    from_='+15165308896 ',
                    to=phone_number
                )
            return redirect('submitOtp')
        else:
            messages.info(request, 'The phone number does not exist', extra_tags="phone_number_otp_error")
            return render(request, 'accounts/otpLogin.html')
    else:
        return render(request, 'accounts/otpLogin.html')



def submitOtp(request):
    if request.method == 'POST':
        otp_user = request.POST['otp']
        if str(random_otp) == otp_user:
            auth.login(request, verified_user)
            return redirect('home')
        else:
            print("not equal")
            messages.info(request, 'Invalid Otp', extra_tags="invalid_otp")
            return render(request, 'accounts/submitOtp.html')
    else:
        return render(request, 'accounts/submitOtp.html')








@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')



# def activate(request, uidb64, token):
#     return HttpResponse(request, 'ok')


@login_required(login_url = 'login')
def dashboard(request):
    user = request.user
    orders = Orders.objects.order_by('-date').filter(user_id=user)
    orders_count = orders.count()
    context = {
        'orders_count':orders_count,
        'orders': orders
    }
    return render(request, 'accounts/dashboard.html',context)



def cancel_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    order.status = 'Cancelled'
    order.save()
    return redirect(dashboard)





def my_account(request):
    user = request.user
    user_details = Account.objects.all().filter(email=user)
    context = {
        'user_details':user_details
    }
    return render(request, 'accounts/my_account.html',context)


def editprofile(request, user_id):
    if request.method=='POST':
        # user = request.user
        edit_details = Account.objects.get(id=user_id)
        if request.POST.get('edit_firstname') != None and request.POST.get('edit_firstname') != "":
            first_name = request.POST['edit_firstname']
            edit_details.first_name = first_name
            edit_details.save()
        if request.POST.get('edit_lastname') != None and request.POST.get('edit_lastname') != "":
            last_name = request.POST['edit_lastname']
            edit_details.last_name = last_name
            edit_details.save()
        if request.POST.get('edit_email') != None and request.POST.get('edit_email') != "":
            email = request.POST['edit_email']
            edit_details.email = email
            edit_details.save()
        if request.POST.get('edit_phonenumber') != None and request.POST.get('edit_phonenumber') != "":
            if len(request.POST.get('edit_phonenumber'))==10:
                phone_number = request.POST['edit_phonenumber']
                edit_details.phone_number = phone_number
                edit_details.save()
            else:
                messages.error(request, 'Enter Valid Mobile Number')
                user = request.user
                user_detail = Account.objects.all().filter(email=user)
                context = {
                    'user_detail':user_detail
                }
                return render(request, 'accounts/edit_profile.html', context)

        return redirect(my_account)
    else:
        user = request.user
        user_detail = Account.objects.all().filter(email=user)
        context = {
            'user_detail':user_detail
        }
        return render(request, 'accounts/edit_profile.html', context)



def address_management(request):
    email = request.user
    user_instance = Account.objects.get(email=email) 
    address = UserAddress.objects.filter(user=user_instance)

    context = {
        'address':address
    }

    return render(request, 'accounts/address_management.html',context)


def add_new_address(request):
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
            return redirect('address_management')
        else:
            if first_name=="":
                messages.error(request, 'Enter first Name')
                return redirect(add_new_address)
            if country=="":
                messages.error(request, 'Select your country')
                return redirect(add_new_address)
            if street_address=="":
                messages.error(request, 'Enter Your Adress properly')
                return redirect(add_new_address)
            if postcode=="":
                messages.error(request, 'Enter your post code')
                return redirect(add_new_address)
            if phone_number=="":
                messages.error(request, 'Enter your phone number')
                return redirect(add_new_address)
            if email=="":
                messages.error(request, 'Enter email address')
                return redirect(add_new_address)
            if len(phone_number)!=10:
                messages.error(request, 'Enter a Valid Phone Number')
                return redirect(add_new_address)

    else:
        return render(request, 'accounts/add_new_address.html')



def change_password(request):
    if request.method=='POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        print('password: ',user.password)
        if new_password==confirm_password and len(new_password)>=5:
            success = user.check_password(old_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Changed')
                return redirect(login)
            else:
                messages.error(request, 'Enter valid current password')
                return redirect(change_password)
        else:
            if new_password!=confirm_password: 
                messages.error(request,'password does not match')
                return redirect(change_password)
            if len(new_password)<=5: 
                messages.error(request,'Enter atleast 5 letters')
                return redirect(change_password)
            return redirect(change_password)

    else:
        return render(request, 'accounts/change_password.html')