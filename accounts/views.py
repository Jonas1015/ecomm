from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.contrib.messages.views import SuccessMessageMixin

from .models import TraderProfile, CustomerProfile
from .forms import TraderProfileUpdateForm, CustomerProfileUpdateForm


from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, reverse, render
from accounts.models import CustomUser
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string
from django.conf import settings

from .forms import CustomerSignUpForm, TraderSignUpForm
from .models import CustomerProfile, TraderProfile
from .tokens import account_activation_token


# class UserLoginView(LoginView):
#     template_name = 'accounts/login.html'
#
#     def get_success_url(self):
#         url = self.get_redirect_url()
#         if url:
#             return url
#         else:
#             return f'/superuser/'


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class SignUpView(TemplateView):
    template_name = 'accounts/register.html'


class CustomerSignUpView(View):

    def get(self, request):
        return render(request, 'accounts/customer_signup.html', {
            'form': CustomerSignUpForm,
        })

    def post(self, request):
        if request.method == 'POST':
            form = CustomerSignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.email = form.cleaned_data['email']
                user.save()
                # Create profile
                customer_profile = CustomerProfile(user=user)
                customer_profile.save()
                # send confirmation email
                token = account_activation_token.make_token(user)
                user_id = urlsafe_base64_encode(force_bytes(user.id))
                url = 'localhost:8000' + reverse('accounts:confirm-email', kwargs={'user_id': user_id, 'token': token})
                message = get_template('accounts/account_activation_email.html').render({
                    'confirm_url': url
                })
                mail = EmailMessage('Shoppy Account Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
                mail.content_subtype = 'html'
                mail.send()

        return render(request, 'accounts/registration_pending.html', {
                    'message': f'A confirmation email has been sent to your email. Please confirm to finish registration.'
                })


class TraderSignUpView(View):

    def get(self, request):
        return render(request, 'accounts/trader_signup.html', {
            'form': TraderSignUpForm,
        })

    def post(self, request):
        if request.method == 'POST':
            form = TraderSignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.email = form.cleaned_data['email']
                user.save()
                # Create profile
                trader_profile = TraderProfile(user=user)
                trader_profile.save()
                # send confirmation email
                token = account_activation_token.make_token(user)
                user_id = urlsafe_base64_encode(force_bytes(user.id))
                url = 'localhost:8000' + reverse('accounts:confirm-email', kwargs={'user_id': user_id, 'token': token})
                message = get_template('accounts/account_activation_email.html').render({
                    'confirm_url': url
                })
                mail = EmailMessage('Shoppy Account Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
                mail.content_subtype = 'html'
                mail.send()

        return render(request, 'accounts/registration_pending.html', {
                    'message': f'A confirmation email has been sent to your email. Please confirm to finish registration.'
                })

class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))

        user = CustomUser.objects.get(pk=user_id)

        context = {
            'message': 'Registration confirmation error. Please click the resend email to generate a new confirmation email.'
        }

        if user and account_activation_token.check_token(user, token):
            user.is_active=True
            user.save()
            context['message'] = 'Registration complete. Please login'

        return render(request, 'accounts/registration_complete.html', context)



class TraderHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = '../ecomm_app/templates/home.html'

    def test_func(self):
        if self.request.user.is_trader:
            return True
        return False


class TraderProfileView(DetailView):
    model = TraderProfile
    template_name = 'accounts/trader_profile.html'
    context_object_name = 'trader_profile'


class TraderProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = TraderProfile
    form_class = TraderProfileUpdateForm
    success_message = "Your profile has been updated successful."

    def test_func(self):
        if self.request.user.traderprofile == TraderProfile.objects.get(user_id=self.kwargs['pk']):
            return True
        return False


class CustomerHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = '../ecomm_app/templates/home.html'

    def test_func(self):
        if self.request.user.is_customer:
            return True
        return False


class CustomerProfileView(DetailView):
    model = CustomerProfile
    template_name = 'accounts/customer_profile.html'
    context_object_name = 'customer_profile'


class CustomerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = CustomerProfile
    form_class = CustomerProfileUpdateForm
    success_message = "Your profile has been updated successful."


    def test_func(self):
        if self.request.user.customerprofile == CustomerProfile.objects.get(user_id=self.kwargs['pk']):
            return True
        return False
