from django.shortcuts import render, reverse
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem, Order
# Create your views here.
from django.shortcuts import get_object_or_404, redirect

import requests
import time






def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            total_price = 0
            for item in cart:
                OrderItem.objects.create(order=order,
                                product=item['product'],
                                price=item['price'],
                                quantity=item['quantity'],
                )
                total_price += item['price'] * item['quantity']
            cart.clear()
            
#  ----------------Payment Integration---------------------------# 
            request.session['total_price'] = f"{total_price}"
            return redirect(reverse('payment:payment_process', args=[order.id]))
            
            
        return render(request, 'payment/canceled.html',{'section':"Some Error with payment , Your order has not been cancelled yet..."})
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html',{'cart':cart, 'form':form})







        



