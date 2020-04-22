from django import forms
from accounts.admin import UserCreationForm
from django.db import transaction
from .models import CustomUser
from .models import TraderProfile, CustomerProfile, AdminProfile
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

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


class UserLoginForm(forms.Form):
    query = forms.CharField(label = 'Username/Email')
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid Credentials - User does not exist!")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("Credentials are not correct!")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)



class TraderProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = TraderProfile
        fields = ['phone_number', 'company', 'region', 'district',  'street_village', 'country','profile_pic', ]

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', ]


class CustomerProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = ['phone_number','region', 'district',  'street_village', 'country','profile_pic', ]


class AdminProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = AdminProfile
        fields = ['phone_number', 'company', 'region', 'district',  'street_village', 'country','profile_pic', ]
