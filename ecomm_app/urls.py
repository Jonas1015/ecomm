from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    OrderSummaryView,
    CheckoutView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    add_single_item_to_cart,
    remove_item_from_cart,
)


app_name = 'ecomm_app'

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('product/<slug>/', ItemDetailView.as_view(), name = 'product'),
    path('order-summary/', OrderSummaryView.as_view(), name = 'order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name = 'remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_item_from_cart, name = 'remove-item-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name = 'remove-single-item-from-cart'),
    path('add-single-item-to-cart/<slug>/', add_single_item_to_cart, name = 'add-single-item-to-cart'),
    path('checkout/', CheckoutView.as_view(), name = 'checkout'),
]
