from django import forms
from django_countries.fields import CountryField

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
