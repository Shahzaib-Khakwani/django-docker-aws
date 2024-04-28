from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import HttpResponse

from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem, Order

import requests
import time
from xhtml2pdf import pisa

# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html', {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     weasyprint.HTML(string = html).write_pdf(response)
    
#     return response

@staff_member_required
def admin_order_pdf(request, order_id):
  order = get_object_or_404(Order, id=order_id)
  print(order.get_total_cost())
  html = render_to_string('orders/order/pdf.html', {'order': order})

  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

  result = pisa.CreatePDF(
      html.encode('UTF-8'), 
      dest=response,
      link_callback=lambda url, rel: None
  )

  if not result.err:
      return response
  else:
      raise Exception("Error generating PDF: %s" % result.err)

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return  render(request, 'admin/orders/order/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            total_price = 0
            for item in cart:
                OrderItem.objects.create(order=order,
                                product=item['product'],
                                price=item['price'],
                                quantity=item['quantity'],
                )
            #     total_price += item['price'] * item['quantity']
            cart.clear()
            
#  ----------------Payment Integration---------------------------# 
            print(cart.get_total_price_after_discount())
            request.session['total_price'] = f"{cart.get_total_price_after_discount()}"
            print(request.session.get("total_price"))
            return redirect(reverse('payment:payment_process', args=[order.id]))
            
            
        return render(request, 'payment/canceled.html',{'section':"Some Error with payment , Your order has not been cancelled yet..."})
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html',{'cart':cart, 'form':form})







        



