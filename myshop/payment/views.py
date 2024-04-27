from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages

import time
import requests
import decimal

from orders.models import Order
from orders.tasks import order_created

# Create your views here.

def payment_process(request, id):
    order = get_object_or_404(Order, id=id)
    
    transaction_id = str(order.id)+"!"+str(int(time.time()))
    request.session['transaction_id'] = transaction_id
    data = {
        'email': "demoqco@sun-fish.com",
        'language':  "EN",
        'pay_to_email': "demoqco@sun-fish.com",
        'transaction_id': transaction_id,
        'amount': decimal.Decimal(request.session.get('total_price')),
        'currency': "USD",
        'status_url':  request.build_absolute_uri(reverse("payment:payment_status_webhook", args=[order.id])),
        'status_url2':  request.build_absolute_uri(reverse("payment:payment_status_webhook", args=[order.id])),
        'return_url':  request.build_absolute_uri(reverse("payment:payment_created", args=[order.id])), 
        'cancel_url':  request.build_absolute_uri(reverse("payment:payment_cancelled", args=[order.id])),
        "prepare_only":1,
        
    }

    url = 'https://pay.skrill.com'

    print(data)
    response = requests.post(url, data=data)
    
    print("-------------------------")
    print(response.text)
    if response.status_code == 200:
        response_data = response.text
        # print(response_data)
        return redirect(f'https://pay.skrill.com/?sid={response_data}')
   


def payment_status(request,id):
  print("reached1")
  if request.method == 'POST':
    transaction_id = request.POST.get('transaction_id')
    amount = request.POST.get('mb_amount')
    status = request.POST.get('status')

    print("reached")
    if status == 2:

        print(request.session.get('transaction_id'))
        order = get_object_or_404(Order, id=id)
        if transaction_id == order.transaction_id:
            total_price = 0
            print("goot session transaction id")
            for item in order.items:
                total_price += item.price * item.quantity
            if total_price == amount:
                order.paid = True
                order.save(update_fields=['paid'])
                messages.success(request, "Payment Done Successfully, Ordered will be delivered soon!!!!!")
        else:
            messages.success(request, "Payment Done Successfully, Ordered will be delivered soon!!!!!")
    elif status == 0:
        messages.success(request, "Payment is Pending!!!!!")
    elif status == -1:
        messages.success(request, "Payment is Cnacelled!!!!!")
    



    return HttpResponse()

  return HttpResponseBadRequest()



def created(request, id):
    order = get_object_or_404(Order, id=id)
    order.transaction_id = request.session.get("transaction_id")
    order.save(update_fields=['transaction_id'])
    # order_created.delay(order.id, order.email)
    return render(request, 'payment/created.html',{'order':order})

def cancelled(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return render(request, 'payment/canceled.html', {'section':"Your order has not been completed..."})

