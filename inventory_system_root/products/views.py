import json
import uuid

from django.core.serializers import serialize
from django.http import HttpResponse
from .models import Products
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db import models

'''def product(request, pk=None):
    if request.method == 'GET':
        if pk is not None:

            # 1. Get product details from DB based on PK value

            product = Products.objects.get(id=pk)

            # 2. Convert Model Object into DICT (Manually)

            product_dict = {
                "id" : product.id,
                "proid" : product.ProductID,
                "procode" : product.ProductCode,
                "proname" : product.ProductName,
                "proimage" : product.ProductImage,
                "procreated" : product.CreatedDate,
                "proupdated" : product.UpdatedDate,
                "prouser" : product.CreatedUser,
                "profav" : product.IsFavourite,
                "prohsn" : product.HSNCode,
                "prostock" : product.TotalStock,
            }

            # 3. Convert DICT Into JSON (dumps())

            product_json = json.dumps(product_dict)

            return HttpResponse(product_json, content_type='application/json')

        else:
            products = Products.objects.all()

            pros_json_metadata = serialize('json', products)
            pros_json = parse_output(pros_json_metadata)

            return HttpResponse(pros_json, content_type='application/json')

    elif request.method == 'POST':

        pro_input_json = request.body

        pro_input_dict = json.loads(pro_input_json)

        id = pro_input_dict.get('id')
        pid = pro_input_dict.get('proid')
        code = pro_input_dict.get('procode')
        name = pro_input_dict.get('proname')
        image = pro_input_dict.get('proimage')
        created = pro_input_dict.get('procreated')
        updated = pro_input_dict.get('proupdated')
        user = pro_input_dict.get('prouser')
        fav = pro_input_dict.get('profav') == 'on'
        hsn = pro_input_dict.get('prohsn')
        stock = pro_input_dict.get('prostock')

        product = Products(id=id, ProductID=pid, ProductCode=code, ProductName=name, ProductImage=image, CreatedDate=created, UpdatedDate=updated, CreatedUser=user, IsFavourite=fav, HSNCode=hsn, TotalStock=stock)

        product.save()

        res_dict = {"message": "Product Created Successfully"}
        res_json = json.dumps(res_dict)

        return HttpResponse(res_json, content_type="application/json")


    elif request.method == 'PUT':

        #1. Get Input JSON from Request
        pro_in_json = request.body

        #2. Convert JSON into DICT
        pro_in_dict = json.loads(pro_in_json)

        #3. Get Employee Data from DB
        pro_db = Products.objects.get(ProductID=pk)

        #4. Merge Input Data into DB Object
        pro_db.pid = pro_in_dict.get('pro_id')
        pro_db.code = pro_in_dict.get('pro_code')
        pro_db.name = pro_in_dict.get('pro_name')
        pro_db.image = pro_in_dict.get('pro_image')
        pro_db.created = pro_in_dict.get('pro_created')
        pro_db.updated = pro_in_dict.get('pro_updated')
        pro_db.user = pro_in_dict.get('pro_user')
        pro_db.fav = pro_in_dict.get('pro_fav')
        pro_db.hsn = pro_in_dict.get('pro_hsn')
        pro_db.stock = pro_in_dict.get('pro_stock')
        pro_db.save()

        # 5. Send Success Response to Client Employee Created Successfully
        res_dict = {"message": "Product Updated Successfully"}
        res_json = json.dumps(res_dict)
        return HttpResponse(res_json, content_type="application/json")'''

def list_products(request):
    products_db = Products.objects.all()

    context_data = {
        "products" : products_db
    }

    return render(request, 'products/product_list.html', context=context_data)

def create_product(request, pk=None):

    if request.method == 'GET':
        if pk is None:
            form = Products()
        else:
            product = Products.objects.get(id=pk)
            form = Products(instance=product)
        return render(request, 'products/product_form.html', {'form': form})
    elif request.method == 'POST':

        id = request.POST.get('pro_id')
        code = request.POST.get('pro_code')
        name = request.POST.get('pro_name')
        image = request.POST.get('pro_image')
        created = request.POST.get('pro_created')
        updated = request.POST.get('pro_updated')
        user = request.user if request.user.is_authenticated else User.objects.get(username='defaultuser')
        fav = request.POST.get('pro_fav') == 'on'
        hsn = request.POST.get('pro_hsn')
        stock = request.POST.get('pro_stock')

        product = Products(ProductID=id, ProductCode=code, ProductName=name, ProductImage=image, CreatedDate=created, UpdatedDate=updated, CreatedUser=user, IsFavourite=fav, HSNCode=hsn, TotalStock=stock)

        product.save()

    return HttpResponse("<h1 style='color : green'>Product Created Successfully</h1>")

def delete_product(request):
    if request.method == 'GET':
        return render(request, 'products/delete_product.html')
    elif request.method == 'POST':
        id_input = request.POST.get('pro_pk')
        try:

            product = Products.objects.get(ProductID=id_input)
            product.delete()
            resp_msg = "<h1 style='color : green'>Product Deleted Successfully</h1>"

        except Exception:
            resp_msg = "<h1 style='color : red'>Ops! Employee with ID did not found</h1>"

        return HttpResponse(resp_msg)

def update_product(request):
    if request.method == 'GET':
        return render(request, 'products/update_product.html')
    elif request.method == 'POST':
        id = request.POST.get('pro_id')
        product = get_object_or_404(Products, ProductID=id)

        code = request.POST.get('pro_code')
        name = request.POST.get('pro_name')
        image = request.FILES.get('pro_image')
        updated = request.POST.get('pro_updated')
        fav = request.POST.get('pro_fav') == 'on'
        hsn = request.POST.get('pro_hsn')
        stock = request.POST.get('pro_stock')

        if code:
            product.ProductCode = code
        if name:
            product.ProductName = name
        if image:
            product.ProductImage = image
        if updated:
            product.UpdatedDate = updated
        product.IsFavourite = fav
        if hsn:
            product.HSNCode = hsn
        if stock:
            product.TotalStock = stock

        product.save()

        return HttpResponse("<h1 style='color : green'>Product Updated Successfully</h1>")

'''def parse_output(products_json_with_metadata):

    products_dict_with_metadata = json.loads(products_json_with_metadata)
    product_list = []
    for pro_dict_with_metadata in products_dict_with_metadata:
        product = pro_dict_with_metadata['fields']
        product['id'] = pro_dict_with_metadata['pk']
        product_list.append(product)

    product_list_json = json.dumps(product_list)
    return product_list_json'''

