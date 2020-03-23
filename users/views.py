from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
# Register users
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # Testing validity and saving
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
        # Displaying success message and redirecting to login form
            messages.success(request, f'Your account has been created successfully! You are now able to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'users/register.html', context)

    #Rendering to the profie template
@login_required
def profile(request):
    profile = Profile.objects.get_or_create(user = request.user)
    u_form = UserUpdateForm(instance = request.user)
    # p_form = ProfileUpdateForm(instance = request.user)
    p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)

    #Update forms for the profile
@login_required
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm( request.POST,
                                    request.FILES,
                                    instance = request.user.profile)

    #Saving my newly updated forms
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You have successfully updated your profile! ')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
        context = {
            'u_form' : u_form,
            'p_form' : p_form
        }
        return render(request, 'users/update.html', context)
