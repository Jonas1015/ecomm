from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    status = forms.CharField(max_length = 100)
    email = forms.EmailField()
    # SEX_CHOICES = (
    #     ('F', 'Female',),
    #     ('M', 'Male',),
    #     ('U', 'Unsure',),
    # )
    # sex = forms.CharField(null = True, max_length=1, choices = SEX_CHOICES)
    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
