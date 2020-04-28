from django.urls import path
# from . import views
from .views import (
    HomeView,
    ItemDetailView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_item_from_cart,
    remove_single_item_from_cart,
    add_single_item_to_cart,
    CheckoutView,

    dashboard,
    orders,

    list_item,
    add_item,
    update_item,
    delete_item,

    list_category,
    add_category,
    update_category,
    delete_category,

    list_subcategory,
    add_subcategory,
    update_subcategory,
    delete_subcategory,
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
    # Staff Urls
    path('staff/dashboard/',dashboard, name = 'dashboard'),
    path('staff/orders/',orders, name = 'orders'),
    path('staff/items/',list_item, name = 'list_item'),
    path('staff/add-item/',add_item, name = 'add_item'),
    path('staff/update-item/<slug>/',update_item, name = 'update_item'),
    path('staff/delete-item/<slug>/',delete_item, name = 'delete_item'),

    path('staff/categories/',list_category, name = 'list_category'),
    path('staff/add-category/',add_category, name = 'add_category'),
    path('staff/add-category/<int:id>/',update_category, name = 'update_category'),
    path('staff/add-category/<int:id>/',delete_category, name = 'delete_category'),

    path('staff/subcategories/',list_subcategory, name = 'list_subcategory'),
    path('staff/add-subcategory/',add_subcategory, name = 'add_subcategory'),
    path('staff/update-subcategory/<int:id>/',update_subcategory, name = 'update_subcategory'),
    path('staff/delete-subcategory/<int:id>/',delete_subcategory, name = 'delete_subcategory'),
]
