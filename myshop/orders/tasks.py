from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from myshop.celery import app

@shared_task
def order_created(order_id, email_address):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    # order = Order.objects.get(id=order_id)
    # subject = f'Order nr. {order.id}'
    # message = f'Dear {order.first_name},\n\n' \
    # f'You have successfully placed an order.' \
    # f'Your order ID is {order.id}.'
    # mail_sent = send_mail(subject,
    # message,
    # 'ak0164051217@gmail.com',
    # [order.email])
    # return mail_sent
    send_mail(
        "Your Feedback",
        f"\t{order_id}\n\nThank you!",
        "ak0164051217@gmail.com",
        [email_address],
        fail_silently=False,
    )

    
