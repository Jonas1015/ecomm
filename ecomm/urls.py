"""ecomm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from users import views as user_views
from django.conf.urls.static import static


urlpatterns = [
    path('', include('ecomm_app.urls', namespace = 'ecomm_app')),
    path('admin/', admin.site.urls),
    # path('register/', user_views.register, name= 'register'),
    # path('profile/', user_views.profile, name= 'profile'),
    # path('login/', auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name = 'login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name = 'accounts/logout.html'), name = 'logout'),
    # path('profile/update/',user_views.update, name='update'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


#
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path('__debug__', include(debug_toolbar.urls))]
