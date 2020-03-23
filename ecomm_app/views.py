from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import CheckoutForm
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress

# Create your views here.
class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'ecomm/home.html'


# @login_required
# class OrderSummaryView(LoginRequiredMixin, View):
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                'object' : order
            }
            return render(self.request, 'ecomm/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = 'ecomm/product.html'


# @login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("ecomm_app:product", slug = slug)
        else:
            order_item.quantity += 1
            order.items.add(order_item)
            order_item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect("ecomm_app:product", slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order.item)
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("ecomm_app:product", slug = slug)


def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("ecomm_app:order-summary")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("ecomm_app:product", slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order.item)
        messages.info(request, "This item was added to your cart.")
        return redirect("ecomm_app:product", slug = slug)


# @login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.quantity = 0
            order_item.save()
            messages.info(request, "This item was removed to your cart.")
            return redirect("ecomm_app:product", slug = slug)
        else:
            # add a message which says the order does not contain the order item
            messages.info(request, "This item was not in your cart")
            return redirect("ecomm_app:product", slug = slug)

    else:
        #add a message saying the user doesnt have an order
        messages.info(request, "You do not have an active order.")
        return redirect("ecomm_app:product", slug = slug)


# @login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.quantity = 0
            order_item.save()
            messages.info(request, "This item was removed to your cart.")
            return redirect("ecomm_app:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecomm_app:product", slug = slug)

    else:
        #add a message saying the user doesnt have an order
        messages.info(request, "You do not have an active order.")
        return redirect("ecomm_app:product", slug = slug)


# @login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity <= 0:
                order.items.remove(order_item)
                messages.info(request, "This item was removed to your cart.")
                return redirect("ecomm_app:order-summary")
            messages.info(request, "This item quantity was updated.")
            return redirect("ecomm_app:order-summary")
        else:
            # add a message which says the order does not contain the order item
            messages.info(request, "This item was not in your cart")
            return redirect("ecomm_app:product", slug = slug)

    else:
        #add a message saying the user doesnt have an order
        messages.info(request, "You do not have an active order.")
        return redirect("ecomm_app:product", slug = slug)


# Checkout View
class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'form': form
        }
        myTemplate = 'ecomm/checkout.html'
        return render(self.request, myTemplate, context )

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                region = form.cleaned_data.get('region')
                country = form.cleaned_data.get('country')

                # TODO: Add functionality to these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    region = region,
                    country = country,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: Add redirect to the selected payment option.
                return redirect('ecomm_app:checkout')
            messages.warning(self.request, "Failed checkout!")
            return redirect('ecomm_app:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("'ecomm_app:checkout'")
