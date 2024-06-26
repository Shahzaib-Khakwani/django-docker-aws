from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from myshop.celery import app
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
from xhtml2pdf import pisa

@shared_task
def order_created(order_id, email_address):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
    f'You have successfully placed an order.' \
    f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
    message,
    'ak0164051217@gmail.com',
    [order.email])
    return mail_sent
    # send_mail(
    #     "Your Feedback",
    #     f"\t{order_id}\n\nThank you!",
    #     "ak0164051217@gmail.com",
    #     [email_address],
    #     fail_silently=False,
    # )

@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
    message,
    'admin@myshop.com',
    [order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    
    result = pisa.CreatePDF(
      html.encode('UTF-8'), 
      dest=out,
      link_callback=lambda url, rel: None
      )

    email.attach(f'order_{order.id}.pdf',
    out.getvalue(),
    'application/pdf')

    email.send()


    
