from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from products.models import Product
from .cart import Cart
from decimal import Decimal


@login_required
def cart_details(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html')


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)

        cartqty = cart.__len__()
        subtotal = cart.get_subtotal_price()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'carttotal':carttotal, 'subtotal':subtotal})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        cartqty = cart.__len__()
        subtotal = cart.get_subtotal_price()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'subtotal':subtotal, 'carttotal': carttotal})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=product_qty)


        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        subtotal = cart.get_subtotal_price()
        response = JsonResponse({'qty': cartqty, 'subtotal':subtotal, 'carttotal': carttotal
        })
        return response

