from django.db.models.base import Model
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from category.models import Category, SubCategory

# Create your views here.


def ParentCategoryList(request):
    parentData = Category.objects.all()
    return render(request, 'admin/parentCategoryList.html', {'parentData': parentData})


def SubCategoryList(request):
    subData = SubCategory.objects.all()
    return render(request, 'admin/subCategoryList.html', {'subData': subData})


def categoryAdd(request):
    if request.method == 'POST':
        if request.POST.get('parent_category_id') == None:
            category_name = request.POST['category_name']
            slug = category_name.replace(" ", "-")
            category_description = request.POST['category_description']
            if category_name != "" and category_description != "":
                category = Category(category_name=category_name,
                                    slug=slug, descrption=category_description)
                category.save()
                return redirect(ParentCategoryList)
            else:
                category_data = Category.objects.all()
                return render(request, 'admin/parentCategory.html', {"category_data": category_data})
        else:
            category_name = request.POST['category_name']
            slug = category_name.replace(" ", "-")
            category_description = request.POST['category_description']
            parent_category_id = request.POST['parent_category_id']
            if category_name != "" and category_description != "":

                category_instance = Category.objects.get(id=parent_category_id)
                category = SubCategory(category_name=category_name,
                                       slug=slug, descrption=category_description, category_id=category_instance)
                category.save()
                return redirect(SubCategoryList)
            else:
                category_data = Category.objects.all()
                return render(request, 'admin/subCategory.html.html', {"category_data": category_data})
    else:
        category_data = Category.objects.all()
        return render(request, 'admin/categoryAdd.html', {"category_data": category_data})


def parentCategoryAdd(request):
    if request.method == 'POST':
        category_name = request.POST['category_name'].lower()
        slug = category_name.replace(" ", "-").lower()
        description = request.POST['description'].lower()
        categorysave = Category()
        categorysave.category_name = category_name
        categorysave.slug = slug
        categorysave.description = description
        categorysave.save()
        return redirect('ParentCategoryList')


    else:
        return render(request, 'admin/parentCategoryAdd.html')





def parentCategoryEdit(request, parent_category_id):
    if request.method == 'POST':
        category = Category.objects.get(id=parent_category_id)
        category_name = request.POST['category_name']
        category_description = request.POST['category_description']
        slug = category_name.replace(" ", "-")
        if category_name != "":
            category.category_name = category_name
            category.slug = slug
        if category_description != "":
            category.category_description = category_description
        category.save()
        print("parent cat updated")
        return redirect(ParentCategoryList)
    else:
        place_holder_data = Category.objects.get(id=parent_category_id)
        return render(request, 'admin/parentCategoryEdit.html', {"place_holder_data": place_holder_data})


def subCategoryEdit(request, sub_category_id):
    if request.method == 'POST':
        if request.POST.get('parent_category_id') == None:
            messages.info(request, 'Please Select a Parent category',
                          extra_tags="select_parent_category")
            place_holder_data = SubCategory.objects.get(id=sub_category_id)
            category_data = Category.objects.all()
            return render(request, 'admin/subCategoryEdit.html', {"category_data": category_data, "place_holder_data": place_holder_data})
        else:
            category = SubCategory.objects.get(id=sub_category_id)
            category_name = request.POST['category_name']
            category_description = request.POST['category_description']
            slug = category_name.replace(" ", "-")
            if category_name != "":
                category.category_name = category_name
                category.slug = slug
            if category_description != "":
                category.category_description = category_description
            category.save()
            print("parent cat updated")
            return redirect(SubCategoryList)
    else:
        place_holder_data = SubCategory.objects.get(id=sub_category_id)
        category_data = Category.objects.all()
        return render(request, 'admin/subCategoryEdit.html', {"category_data": category_data, "place_holder_data": place_holder_data})


def parentCategoryDelete(request, parent_category_id):
    Category.objects.filter(id=parent_category_id).delete()
    return redirect(ParentCategoryList)


def subCategoryDelete(request, sub_category_id):
    SubCategory.objects.filter(id=sub_category_id).delete()
    return redirect(SubCategoryList)
