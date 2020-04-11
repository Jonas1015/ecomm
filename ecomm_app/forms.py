from django import forms
from django_countries.fields import CountryField
from .models import (
        Item,
        OrderItem,
        Order,
        Category,
        Subcategory,
        BillingAddress,
)

PAYMENT_CHOICES = {
    ('MP', 'M-PESA'),
    ('TP', 'Tigo-PESA'),
    ('PP', 'PAYPAL'),
}

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1224 main st'
    }))
    region = forms.CharField(required = False, widget=forms.TextInput(attrs={
        'placeholder': 'Dar, Temeke'
    }))
    country = CountryField(blank_label = 'Select Country').formfield()
    same_billing_address = forms.BooleanField(required = False, widget = forms.CheckboxInput())
    save_info = forms.BooleanField(required = False, widget = forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget = forms.RadioSelect, choices = PAYMENT_CHOICES)



class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'image')

class addSubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ('category', 'name', 'image')

class addItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        exclude = ('seller', 'slug',)
        fields = ('category', 'title', 'price', 'discount_price', 'label', 'tag', 'image1', 'image2', 'image3', 'description')
