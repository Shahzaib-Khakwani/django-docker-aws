from django.urls import path
from . import views

app_name = 'payment'


urlpatterns = [
    path("payment/<int:id>/", views.payment_process, name= "payment_process"),
    path("created/<int:id>/", views.created, name= "payment_created"),
    path("cancelled/<int:id>/", views.cancelled, name= "payment_cancelled"),
    path("status/<int:id>/", views.payment_status, name= "payment_status_webhook"),
]