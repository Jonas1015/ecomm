from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
import random
from .forms import (
        CheckoutForm,
        addCategoryForm,
        addSubcategoryForm,
        addItemForm,
)
from .models import (
        Item,
        OrderItem,
        Order,
        Category,
        Subcategory,
        BillingAddress,
)

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
            messages.warning(self.request, "You do not have an active order")
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
            messages.warning(self.request, "You do not have an active order")
            return redirect("'ecomm_app:checkout'")

# For Admin Panel
# ITEMS

def list_item(request):
    all_items = Item.objects.filter(seller = request.user.id).order_by('id')
    query = request.GET.get("q")
    if query:
        all_items = all_items.filter(title__icontains = query)
    context = {
        'items': all_items
    }
    myTemplate = 'ecomm/listItem.html'
    return render (request, myTemplate, context)

def add_item(request):
    # form = addItemForm()
    if request.method == 'POST':
        form = addItemForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit = False)
            form.seller = request.user
            form.save()
            messages.success(request, f'Item added successfully')
            return redirect('ecomm_app:add_item')
        # return redirect('ecomm_app:add_item')
    else:
        form = addItemForm()
    context = {
        'form': form
    }
    myTemplate = 'ecomm/addItem.html'
    return render(request, myTemplate, context)

def update_item(request, slug):
    instance = get_object_or_404(Item, slug = slug)
    form = addItemForm(request.POST or None, instance = instance)
    # print(form.product_name)
    if request.method == 'POST':
        form = addItemForm(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save(commit = False)
            form.seller = request.user
            form.save()
            messages.success(request, f'Item has been updated successifully!')
            return redirect ('ecomm_app:home')
    context = {
        'form': form,
    }
    myTemplate = 'ecomm/updateItem.html'
    return render(request, myTemplate, context)


def delete_item(request, slug):
    get_data = get_object_or_404(Item, slug = slug)
    get_data.delete()
    messages.success(request, f'Item deleted successfull!')
    return redirect('ecomm_app:home')


# CATEGORY
def list_category(request):
    all_categories = Category.objects.all().order_by('id')
    query = request.GET.get("q")
    if query:
        all_categories = all_categories.filter(name__icontains = query)
    context = {
    'categories': all_categories
    }
    myTemplate = 'ecomm/listCategory.html'
    return render (request, myTemplate, context)

def add_category(request):
    form = addCategoryForm()
    if request.method == 'POST':
        form = addCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category added successfully')
            return redirect('ecomm_app:add_category')
        return redirect('ecomm_app:add_category')
    else:
        form = addCategoryForm()
    context = {
        'form': form
    }
    myTemplate = 'ecomm/addCategory.html'
    return render(request, myTemplate, context)

def update_category(request, id):
    instance = get_object_or_404(Category, id = id)
    form = addCategoryForm(request.POST or None, instance = instance)
    # print(form.product_name)
    if request.method == 'POST':
        form = addCategoryForm(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category has been updated successifully!')
            return redirect ('ecomm_app:list_category')
    context = {
        'form': form,
    }
    myTemplate = 'ecomm/updateCategory.html'
    return render(request, myTemplate, context)


def delete_category(request, id):
    get_data = get_object_or_404(Category, id = id)
    get_data.delete()
    messages.success(request, f'Category deleted successfully!')
    return redirect('ecomm_app:list_category')


# SUB-CATEGORY
def list_subcategory(request):
    all_subcategories = Subcategory.objects.all().order_by('id')
    query = request.GET.get("q")
    if query:
        all_subcategories = all_subcategories.filter(name__icontains = query)
    context = {
        'subcategories': all_subcategories
    }
    myTemplate = 'ecomm/listSubcategory.html'
    return render (request, myTemplate, context)


def add_subcategory(request):
    form = addSubcategoryForm()
    if request.method == 'POST':
        form = addSubcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sub-Category added successfully')
            return redirect('ecomm_app:add_subcategory')
        return redirect('ecomm_app:add_subcategory')
    else:
        form = addSubcategoryForm()
    context = {
        'form': form
    }
    myTemplate = 'ecomm/addSubcategory.html'
    return render(request, myTemplate, context)

def update_subcategory(request, id):
    instance = get_object_or_404(Subcategory, id = id)
    form = addSubcategoryForm(request.POST or None, instance = instance)
    # print(form.product_name)
    if request.method == 'POST':
        form = addSubcategoryForm(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sub-Category has been updated successifully!')
            return redirect ('ecomm_app:list_subcategory')
    context = {
        'form': form,
    }
    myTemplate = 'ecomm/updateSubcategory.html'
    return render(request, myTemplate, context)

def delete_subcategory(request, id):
    get_data = get_object_or_404(Subcategory, id = id)
    get_data.delete()
    messages.success(request, f'Sub-Category deleted successfull!')
    return redirect('ecomm_app:list_subcategory')
