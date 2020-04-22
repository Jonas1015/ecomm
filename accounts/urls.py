from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    # path('login/', views.UserLoginView.as_view(), name='login'),
    # path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'accounts/logout.html'), name = 'logout'),
    path('signup/', views.SignUpView.as_view(), name='register'),
    # path('signup/customer/', views.CustomerSignUpView.as_view(), name='register-customer'),
    path('signup/customer/', views.customer_signup, name='register-customer'),
    path('signup/trader/', views.trader_signup, name='register-trader'),
    # path('signup/trader/', views.TraderSignUpView.as_view(), name='register-trader'),
    path('confirm-email/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm-email'),


    path('profile/', views.ProfileView, name='profile'),
    path('profile/update/', views.ProfileUpdateView, name='profile-update'),
    #
    # path('profile/<int:pk>/', views.CustomerProfileView.as_view(), name='customer-profile'),
    # path('profile/<int:pk>/update/', views.CustomerProfileUpdateView.as_view(), name='customer-profile-update'),
    #
    # path('profile/<int:pk>/', views.TraderProfileView.as_view(), name='trader-profile'),
    # path('profile/<int:pk>/update/', views.TraderProfileUpdateView.as_view(), name='trader-profile-update')
]
