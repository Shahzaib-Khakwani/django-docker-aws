from django.shortcuts import render
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem
# Create your views here.
from .tasks import order_created
from django.core.mail import send_mail
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                product=item['product'],
                                price=item['price'],
                                quantity=item['quantity'],
                )
            cart.clear()
            # order_created(order.id)
            order_created.delay(order.id, order.email)
        return render(request, 'orders/order/created.html',{'order':order})
    else:
        form = OrderCreateForm()

        return render(request, 'orders/order/create.html',{'cart':cart, 'form':form})
        



