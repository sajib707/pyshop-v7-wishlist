from django.http.response import JsonResponse
from django.shortcuts import render

from cart.cart import Cart

from .models import Order, OrderItem


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        carttotal = cart.get_total_price()

        full_name = request.POST.get('full_name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        post_code = request.POST.get('post_code')

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name=full_name,
                address1=address1,
                address2=address2,
                post_code=post_code,
                total_paid=carttotal,
                order_key=order_key
            )
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(request):
    if request.method == 'POST':
        order_key = request.POST.get('order_key')
        try:
            order = Order.objects.get(order_key=order_key)
            order.billing_status = True
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'})
    
    return JsonResponse({'error': 'Invalid request'})


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)#.filter(billing_status=True)
    return orders