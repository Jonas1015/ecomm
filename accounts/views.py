from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template, render_to_string
from django.views.generic import TemplateView, View, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, get_user_model, logout
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from .models import CustomUser
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from .models import (
    TraderProfile,
    CustomerProfile,
    AdminProfile,
)
from .forms import (
    TraderProfileUpdateForm,
    CustomerProfileUpdateForm,
    AdminProfileUpdateForm,
    UserUpdateForm,
    CustomerSignUpForm,
    TraderSignUpForm,
    UserLoginForm,
)


def loginView(request, *args, **kwargs):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            return HttpResponseRedirect('/')
    myTemplate = 'accounts/login.html'
    context = {
        'form':form
    }
    return render(request, myTemplate, context)




class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class SignUpView(TemplateView):
    template_name = 'accounts/register.html'


# class CustomerSignUpView(View):
#
#     def get(self, request):
#         return render(request, 'accounts/customer_signup.html', {
#             'form': CustomerSignUpForm,
#         })
#
#     def post(self, request):
#         if request.method == 'POST':
#             form = CustomerSignUpForm(request.POST or None)
#             if form.is_valid():
#                 user = form.save()
#                 user.email = form.cleaned_data['email']
#                 user.save()
#                 # Create profile
#                 customer_profile = CustomerProfile(user=user)
#                 customer_profile.save()
#                 # send confirmation email
#                 token = account_activation_token.make_token(user)
#                 user_id = urlsafe_base64_encode(force_bytes(user.id))
#                 url = 'localhost:8000' + reverse('accounts:confirm-email', kwargs={'user_id': user_id, 'token': token})
#                 message = get_template('accounts/account_activation_email.html').render({
#                     'confirm_url': url
#                 })
#                 mail = EmailMessage('Shoppy Account Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
#                 mail.content_subtype = 'html'
#                 mail.send()
#
#         return render(request, 'accounts/registration_pending.html', {
#                     'message': f'A confirmation email has been sent to your email. Please confirm to finish registration.'
#                 })

def customer_signup(request):
    form = CustomerSignUpForm(request.POST or None)
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
    # form = CustomerSignUpForm()
    myTemplate = 'accounts/customer_signup.html'
    context ={
        'form': form
    }
    return render(request, myTemplate,context)


def trader_signup(request):
    form = TraderSignUpForm(request.POST or None)
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
    myTemplate = 'accounts/trader_signup.html'
    context ={
        'form': form
    }
    return render(request, myTemplate,context)



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


class CustomerHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = '../ecomm_app/templates/home.html'

    def test_func(self):
        if self.request.user.is_customer:
            return True
        return False

@login_required
def ProfileView(request):

    if request.user.is_admin:
        profile = AdminProfile.objects.get(user = request.user)
    elif request.user.is_customer:
        profile = CustomerProfile.objects.get(user = request.user)
    elif request.user.is_trader:
        profile = TraderProfile.objects.get(user = request.user)
    else:
        message = 'You have no permission to view this page'
        context = {
            'message': message
        }
        return render(request, 'accounts/profile.html', context)
    if profile.phone_number and profile.region and profile.district and profile.street_village:
        profile.user.is_eligible = True
        profile.user.save()
    else:
        profile.user.is_eligible = False
        profile.user.save()
    context = {
        'profile': profile,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def ProfileUpdateView(request):
    user_form = UserUpdateForm(instance = request.user)
    if request.user.is_admin:
        profile_form = AdminProfileUpdateForm(instance = request.user.adminprofile)
        profile = AdminProfile.objects.get(user = request.user)

    elif request.user.is_customer:
        profile_form = CustomerProfileUpdateForm(instance = request.user.customerprofile)
        profile = CustomerProfile.objects.get(user = request.user)

    elif request.user.is_trader:
        profile_form = TraderProfileUpdateForm(instance = request.user.traderprofile)
        profile = TraderProfile.objects.get(user = request.user)

    else :
        messages.warning(request, f'You have no permission to view this page')
        return redirect('ecomm_app:home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)

        if request.user.is_admin:
            profile_form = AdminProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance = request.user.adminprofile)
            profile = AdminProfile.objects.get(user = request.user)

        elif request.user.is_customer:
            profile_form = CustomerProfileUpdateForm(request.POST,
                                        request.FILES, instance = request.user.customerprofile)
            profile = CustomerProfile.objects.get(user = request.user)
        elif request.user.is_trader:
            profile_form = TraderProfileUpdateForm(request.POST,
                                        request.FILES, instance = request.user.traderprofile)
            profile = TraderProfile.objects.get(user = request.user)
        else:
            return redirect('accounts:profile')
            #Saving my newly updated forms
        if profile_form.is_valid() and user_form.is_valid():
            if request.user.is_admin:
                profiles = AdminProfile.objects.all()
            elif request.user.is_customer:
                profiles = CustomerProfile.objects.all()
            elif request.user.is_trader:
                profiles = TraderProfile.objects.all()
            for profile in profiles:
                if profile.phone_number:
                    if profile_form.cleaned_data['phone_number'] == profile.phone_number:
                        messages.info(request, f'This number is already used by someone!')
                        return redirect('accounts:profile-update')
            profile_form.save()
            user_form.save()
            messages.success(request, f'You have successfully updated your profile! ')
            return redirect('accounts:profile')

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
        }
    return render(request, 'accounts/update.html', context)
