from django import forms
from accounts.admin import UserCreationForm
from django.db import transaction
from .models import CustomUser
from .models import TraderProfile, CustomerProfile



class CustomerSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user

class TraderSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_trader = True
        if commit:
            user.save()
        return user




class TraderProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = TraderProfile
        fields = ['phone_number', 'company', 'region', 'district',  'street_village', 'country','profile_pic', ]



class CustomerProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = ['phone_number','region', 'district',  'street_village', 'country','profile_pic', ]
