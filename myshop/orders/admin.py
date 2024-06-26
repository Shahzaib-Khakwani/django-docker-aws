from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

import datetime
import csv

from .models import Order, OrderItem


# Register your models here.

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args = [obj.id])
    return mark_safe(f'<a href={url}>View</a>')

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args = [obj.id])
    return mark_safe(f'<a href={url}>Generate</a>')


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_diposition = f'attachment: filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_diposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row=[]
        for field in fields:
             value = getattr(obj, field.name)
             if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
             data_row.append(value)
        writer.writerow(data_row)
    return response


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email','address', 'postal_code', 'city', 'paid','created', 'updated', order_detail, order_pdf]
    list_filter = ['created','updated','paid']
    inlines = [OrderItemInLine]
    actions = [export_to_csv]

