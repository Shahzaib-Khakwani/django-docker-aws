from django import forms
from django.utils.translation  import gettext_lazy as _
from .models import Order

class  OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [_('first_name'), _('last_name'),_('email'),_('address'),_('postal_code'),_('city')]

        



