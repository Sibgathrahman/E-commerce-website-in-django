from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from admins.views import adminLogin
from carts.models import Carts
from carts.views import cart
import uuid, razorpay
from category.models import Category, SubCategory
from dizzkartproject.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from store.models import Products
# Create your views here.








def product_detail(request, category_name, product_slug):
    try:
        single_product = Products.objects.get(category_name=category_name, slug=product_slug)

        in_cart=Carts.objects.filter(product=single_product).exists()
    except Exception as e:
        # print('working here')
        raise e
        # pass

    context = {
        'single_product': single_product,
        'in_cart':in_cart,
    }

    return render(request, 'store/product_detail.html', context)




def productAdd(request):
    if request.method == 'POST':
        # setup null issues
        product_name = request.POST['product_name']
        slug = product_name.replace(" ", "-")
        product_mrp = request.POST['product_mrp']
        product_sale_price = request.POST['product_sale_price']
        product_stock = request.POST['product_stock']
        product_description = request.POST['product_description']
        if request.POST.get('product_size_XS') != None:
            product_size = "XS"
        if request.POST.get('product_size_S') != None:
            product_size = "S"
        if request.POST.get('product_size_M') != None:
            product_size = "M"
        if request.POST.get('product_size_L') != None:
            product_size = "L"
        if request.POST.get('product_size_XL') != None:
            product_size = "XL"
        # foreign key
        product_category_id = request.POST['product_category_id']
        product_instance = SubCategory.objects.get(id=product_category_id)
        product_image = request.FILES['product_image']

        # product = Products(product_name=product_name, mrp=mrp, sale_price=sales_price, stocks=stock, image =product_cover, sub_category=sub, description=description,Category = cat)
        # product.save()



        product = Products(product_name=product_name, slug=slug, mrp=product_mrp, sale_price=product_sale_price, stock=product_stock, description=product_description, category=product_instance, image=product_image, size=product_size)
        product.save()
        return redirect(productList)
    else:
        data = Category.objects.all()
        sub_data = SubCategory.objects.all()
        contxt = {
            'data': data,
            'sub_data': sub_data
        }
        return render(request, 'products/productAdd.html', contxt)


def productList(request):
    product_data = Products.objects.all()
    return render(request, 'products/productList.html', {'product_data': product_data})


def productEdit(request, product_id):
    if request.method == 'POST':
        product = Products.objects.get(id=product_id)
        print("read this : ", product.product_name)
        if request.POST.get('product_name') != None:
            product_name = request.POST['product_name']
            slug = product_name.replace(" ", "-")
            product.product_name = product_name
            product.slug = slug
        if request.POST.get('product_mrp') != None:
            print("mrp found")
            product_mrp = request.POST['product_mrp']
            product.mrp = product_mrp
        if request.POST.get('product_sale_price') != None:
            product_sale_price = request.POST['product_sale_price']
            product.sale_price = product_sale_price
        if request.POST.get('product_stock') != None:
            product_stock = request.POST['product_stock']
            product.stock = product_stock
        if request.POST.get('product_description') != None:
            product_description = request.POST['product_description']
            product.description = product_description
        if request.POST.get('product_size_XS') != None:
            product_size = "XS"
            product.size = product_size
        if request.POST.get('product_size_S') != None:
            product_size = "S"
            product.size = product_size
        if request.POST.get('product_size_M') != None:
            product_size = "M"
            product.size = product_size
        if request.POST.get('product_size_L') != None:
            product_size = "L"
            product.size = product_size
        if request.POST.get('product_size_XL') != None:
            product_size = "XL"
            product.size = product_size
        if request.POST.get('product_category_id') != None and request.POST.get('product_category_id') != "":
            product_category_id = request.POST['product_category_id']
            product_instance = SubCategory.objects.get(id=product_category_id)
            product.category = product_instance
        if request.FILES.get('product_image') != None and request.POST.get('product_image') != "":
            product_image = request.FILES['product_image']
            product.image = product_image
        product.save()
        return redirect(productList)
    else:
        edit_product_data = Products.objects.get(id=product_id)
        product_data = SubCategory.objects.all()
        return render(request, 'products/productEdit.html', {'edit_product_data': edit_product_data, 'product_data': product_data})


def productDetails(request, product_id):
    return render(request, 'store/store.html')


def productDelete(request, product_id):
    Products.objects.filter(id=product_id).delete()
    return redirect(productList)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(SubCategory, slug = category_slug)
        products = Products.objects.filter(category_name=categories, is_available=True)
        product_count = products.count()

    else:
        products = Products.objects.all().filter(is_available=True)
        product_count = products.count()


    context = {
        'products':products,
        'product_count':product_count,
    }

    return render(request, 'store/store.html', context)