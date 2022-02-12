from django.shortcuts import redirect, render
from .models import CouponOffer
from django.contrib import messages
# Create your views here.


def coupon_offer(request):
    coupon=CouponOffer.objects.all()
    return render(request, 'admin/coupen_list.html',{'data':coupon})



def add_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST['coupon_name']
        coupon_id = request.POST['coupon_id']
        offer_persontage = request.POST['offer_persontage']
        if CouponOffer.objects.filter(coupon_id=coupon_id).exists():
            messages.info(request, 'Coupon Id already taken')
            return redirect(add_coupon)
        coupon = CouponOffer(coupon_name=coupon_name,coupon_id=coupon_id,offer_persantage=offer_persontage)
        coupon.save()
        return redirect(coupon_offer)
    return render(request, 'admin/add_coupon.html')


def coupon_delete(request, coupon_id):
    CouponOffer.objects.filter(id=coupon_id).delete()

    return redirect(coupon_offer)


def edit_coupon(request, coupon_id):
    data = CouponOffer.objects.filter(id=coupon_id)
    # if request.method == 'POST':
    #     coupon_name = request.POST['coupon_name']
    #     coupon_id = request.POST['coupon_id']
    #     offer_persontage = request.POST['offer_persontage']
    #     if CouponOffer.objects.filter(coupon_id=coupon_id).exists():
    #         messages.info(request, 'Coupon Id already taken')
    #         return redirect(add_coupon)
    #     if coupon_name != None:
    #         data.coupon_name=coupon_name
    #         data.save()
    return render(request, 'admin/coupon_edit.html')