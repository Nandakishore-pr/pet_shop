#forms.py
from django import forms
from core.models import ProductOffer,Product,Category,CategoryOffer
from django.forms.widgets import DateInput,TextInput,SelectMultiple


class ProductOfferForm(forms.ModelForm):
    discount_percentage = forms.CharField(widget=TextInput)
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=SelectMultiple, required=True)
    class Meta:
        model = ProductOffer
        fields = ['discount_percentage', 'start_date', 'end_date', 'active','products']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class CategoryOfferForm(forms.ModelForm):
    cat_discount_percentage = forms.CharField(widget=TextInput)
    categorys = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=SelectMultiple,required = True)

    class Meta:
        model = CategoryOffer
        fields = ['cat_discount_percentage', 'cat_start_date', 'cat_end_date','cat_active','categorys']
        widgets = {
            'cat_start_date': DateInput(attrs={'type': 'date'}),
            'cat_end_date': DateInput(attrs={'type': 'date'}),
        }