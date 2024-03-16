# forms.py
from django import forms
from account.models import Address

class AddressSelectionForm(forms.Form):
    shipping_address = forms.ModelChoiceField(queryset=None, empty_label=None,to_field_name='id')

    def __init__(self, user, *args, **kwargs):
        super(AddressSelectionForm, self).__init__(*args, **kwargs)
        self.fields['shipping_address'].queryset = Address.objects.filter(user=user)

class PaymentOptionForm(forms.Form):
    payment_option = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('bank_transfer', 'Bank Transfer'),('cash_on_delivery','cash on delivery')])



class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)