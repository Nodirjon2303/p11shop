from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import *
import json


def homeView(request):
    categories = Category.objects.all()
    data = []
    for i in categories:
        data.append({
            'id': i.id,
            'name': i.name,
            'number_of_products': Product.objects.filter(category=i).count(),
            'image': i.image_url,
            'slug': i.slug
        })
    context = {
        'categories': data,
        'cart': Order_detail.objects.filter(order__status='progress', order__customer=request.user).count()
    }
    return render(request, 'index.html', context)


def shopView(request, slug):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['product_id']
        savatcha, bol = Order.objects.get_or_create(customer=request.user, status='progress')
        order_detail, condition = Order_detail.objects.get_or_create(order=savatcha, product_id=product_id)
        if not condition:
            order_detail.number_of_product += 1
        try:
            order_detail.save()
        except Exception as e:
            return JsonResponse({"data": e.message})
        return JsonResponse({"data": 'ok'})
    try:
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category)
        return render(request, 'shop.html', {"products": products})
    except:
        return render(request, '404.html')


def cartView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data['product_id']
        soni = data['soni']
        order_detail = Order_detail.objects.get(id=product_id)
        order_detail.number_of_product = int(soni)
        try:
            order_detail.save()
        except Exception as e:
            return JsonResponse({"data": e.message})
        print(order_detail.number_of_product)
        return JsonResponse({"data": 'ok', 'total_amount':order_detail.all_price})
    products = Order_detail.objects.filter(order__status='progress', order__customer=request.user)
    context = {
        'products': products,

    }
    return render(request, 'cart.html', context)
